from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.merchant import MerchantCreate, MerchantUpdate, MerchantInDB
from app.db.models.user import User
from app.services.merchant import create_merchant, get_merchants, get_merchant, update_merchant, delete_merchant
from app.dependencies.dependecies import get_current_user, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

@router.post("/", response_model=MerchantInDB)
def create_new_merchant(
    merchant: MerchantCreate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return create_merchant(db=db, merchant=merchant)


@router.get("/", response_model=List[MerchantInDB])
def read_merchants(
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return get_merchants(db=db)


@router.get("/{merchant_id}", response_model=MerchantInDB)
def read_merchant(
    merchant_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_merchant = get_merchant(db=db, merchant_id=merchant_id)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant


@router.put("/{merchant_id}", response_model=MerchantInDB)
def update_existing_merchant(
    merchant_id: int,
    merchant: MerchantUpdate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_merchant = update_merchant(db=db, merchant_id=merchant_id, merchant=merchant)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant


@router.delete("/{merchant_id}")
def delete_existing_merchant(
    merchant_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_merchant = delete_merchant(db=db, merchant_id=merchant_id)
    if db_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return {"detail": "Merchant deleted"}


