from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.config import settings
from app.services.user import authenticate_user
from app.core import security
from app.db.session import SessionLocal
from app.schemas.user import AccessToken, LoginForm, ValidateToken, RefreshToken, LoginToken
from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.dependecies import get_db, get_current_user, get_user_from_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter()

@router.post("/token", response_model=AccessToken)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": security.create_access_token(user.id),
    }

@router.post("/login", response_model=LoginToken)
def login(form_data: LoginForm, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.email, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        return {
            "access_token": security.create_access_token(user.id),
            "refresh_token": security.create_refresh_token(user.id),
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh", response_model=RefreshToken)
def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_user_from_refresh_token(db, refresh_token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer"
    }

@router.get("/validate")
def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = get_current_user(db, token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not Authorized")

    if not user:
        raise HTTPException(status_code=400, detail="Invalid access token")
    return {"detail": "Access token is valid"}