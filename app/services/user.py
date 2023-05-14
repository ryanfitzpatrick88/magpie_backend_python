import jwt
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.user import User
from app.core.security import verify_password, get_password_hash
from datetime import datetime, timedelta
from app.core.config import settings
from app.schemas.user import UserRegister
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.token import TokenData
from app.db.models.user_account import UserAccount

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(db: Session, user: UserRegister):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.email, email=user.email, hashed_password=hashed_password)

    # Create a UserAccount instance
    user_account = UserAccount(
        database=str(uuid4()),  # Generate a random GUID
        alias="account",
        is_active=True,
        is_deleted=False,
    )

    # Associate the UserAccount instance with the User instance
    db_user.user_account = user_account

    # Add the User instance (and the associated UserAccount instance) to the session
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, updated_user: User):
    db_user = db.query(User).filter(User.id == user_id).one()
    db_user.username = updated_user.username
    db_user.email = updated_user.email
    db_user.is_active = updated_user.is_active
    db_user.user_account.database = updated_user.user_account.database
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).one()
    db.delete(db_user)
    db.commit()
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
