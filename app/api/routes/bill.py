from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.bill import BillCreate, BillUpdate, BillInDB
from app.db.models.user import User
from app.services.bill import create_bill, get_bills, get_bill, update_bill, delete_bill
from app.dependencies.dependecies import get_current_user, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

@router.post("/", response_model=BillInDB)
def create_new_bill(
    bill: BillCreate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return create_bill(db=db, bill=bill)


@router.get("/", response_model=List[BillInDB])
def read_bills(
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    return get_bills(db=db)


@router.get("/{bill_id}", response_model=BillInDB)
def read_bill(
    bill_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bill = get_bill(db=db, bill_id=bill_id)
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill


@router.put("/{bill_id}", response_model=BillInDB)
def update_existing_bill(
    bill_id: int,
    bill: BillUpdate,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bill = update_bill(db=db, bill_id=bill_id, bill=bill)
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return db_bill


@router.delete("/{bill_id}")
def delete_existing_bill(
    bill_id: int,
    db: Session = Depends(get_user_db),
    current_user: User = Depends(get_current_user),
):
    db_bill = delete_bill(db=db, bill_id=bill_id)
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {"detail": "Bill deleted"}


