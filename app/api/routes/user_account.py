
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.user_account import UserAccountCreate, UserAccountUpdate, UserAccountInDB
from app.db.models.user_account import UserAccount
from app.db.models.user import User
from app.services.user_account import create_user_account, get_user_accounts, get_user_account, \
    update_user_account, delete_user_account
from app.dependencies.dependecies import get_db, get_current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


@router.get("/", response_model=List[UserAccountInDB])
def read_user_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users_accounts = get_user_accounts(db, skip=skip, limit=limit)
    return users_accounts

@router.post("/", response_model=UserAccountInDB)
def create_user_account_item(user_account: UserAccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user_account(db, user_account)

@router.get("/{user_account_id}", response_model=UserAccountInDB)
def read_user_account(user_account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user_account = get_user_account(db, user_account_id=user_account_id)
    if db_user_account is None:
        raise HTTPException(status_code=404, detail="UserAccount not found")
    return db_user_account

@router.put("/{user_account_id}", response_model=UserAccountInDB)
def update_user_account_item(user_account_id: int, user_account: UserAccountUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user_account = update_user_account(db, user_account_id, user_account)
    if updated_user_account is None:
        raise HTTPException(status_code=404, detail="UserAccount not found")
    return updated_user_account

@router.delete("/{user_account_id}")
def delete_user_account_item(user_account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = delete_user_account(db, user_account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="UserAccount not found")
    return {"detail": "UserAccount deleted successfully"}

