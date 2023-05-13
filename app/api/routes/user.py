from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserRegister, EmailSchema, CheckEmailResponse
from app.db.models.user import User
from app.services.user import create_user, get_users, get_user, update_user, delete_user, get_user_by_username, \
    get_user_by_email
from app.depdendencies.depdendecies import get_db
from app.api.dependencies import get_current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


@router.post("/", response_model=UserInDB)
def create_user_item(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user(db, user)

@router.get("/", response_model=List[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserInDB)
def update_user_item(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user_item(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.post("/register", response_model=UserInDB)
def register_user(user_register: UserRegister, db: Session = Depends(get_db)):
    try:
        return create_user(db, user_register)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/check-email", response_model=CheckEmailResponse)
def check_unique_email(email: EmailSchema, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, email.email)
        return {"emailExists": user is not None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


