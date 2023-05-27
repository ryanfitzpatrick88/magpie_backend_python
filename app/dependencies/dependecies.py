import jwt
from jwt import ExpiredSignatureError
from app.db.session import SessionLocal
from app.db.models.user import User
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.token import TokenData
from app.services.user import get_user
from jwt import decode, exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise expired_exception
    user = get_user(db, int(token_data.username))
    if user is None:
        raise credentials_exception
    return user


def get_user_from_refresh_token(db, token: str) -> User:
    try:
        # Decode the token using the same SECRET_KEY and ALGORITHM as when it was encoded.
        payload = decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except exceptions.PyJWTError as error:
        raise HTTPException(status_code=400, detail=f"Invalid refresh token {str(error)}")

    # Extract the username from the decoded payload.
    id = payload.get("sub")

    # Fetch the user record.
    user = get_user(db, int(id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

def get_user_db(user: User = Depends(get_current_user)) -> Session:
    if user:
        database_url = f'{settings.DATABASE_URL}/{user.user_account.database}'
    else:
        database_url = f'{settings.DATABASE_URL}/users'  # replace with your default url

    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
