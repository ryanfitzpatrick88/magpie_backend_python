from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountInDB
from app.db.models.user import User
from app.services.bank_account import create_bank_account, get_bank_accounts, get_bank_account, update_bank_account, delete_bank_account
from app.dependencies.dependecies import get_current_user, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

@router.post("/", response_model=BankAccountInDB)
def create_new_bank_account(
    bank_account: BankAccountCreate,
    db: Session = Depends(get_user_db),
):
    return create_bank_account(db=db, bank_account=bank_account)


@router.get("/", response_model=List[BankAccountInDB])
def read_bank_accounts(
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return get_bank_accounts(db=db)


@router.get("/{bank_account_id}", response_model=BankAccountInDB)
def read_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bank_account = get_bank_account(db=db, bank_account_id=bank_account_id)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="BankAccount not found")
    return db_bank_account


@router.put("/{bank_account_id}", response_model=BankAccountInDB)
def update_existing_bank_account(
    bank_account_id: int,
    bank_account: BankAccountUpdate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bank_account = update_bank_account(db=db, bank_account_id=bank_account_id, bank_account=bank_account)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="BankAccount not found")
    return db_bank_account


@router.delete("/{bank_account_id}")
def delete_existing_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bank_account = delete_bank_account(db=db, bank_account_id=bank_account_id)
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="BankAccount not found")
    return {"detail": "BankAccount deleted"}


