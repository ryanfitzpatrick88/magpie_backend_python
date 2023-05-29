from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionInDB, TransactionDuplicate
from app.db.models.user import User
from app.schemas.user import UserInDB
from app.services.transaction import create_transaction, get_transactions, get_transaction, update_transaction, \
    delete_transaction, preview_transactions, upload_transactions, delete_transactions_by_batch, \
    get_transactions_by_batch, get_transactions_by_date_range, get_transactions_by_date_range_for_duplicates
from app.dependencies.dependecies import get_current_user, get_user_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


@router.post("/", response_model=TransactionInDB)
def create_transaction_item(transaction: TransactionCreate, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    return create_transaction(db, transaction)

@router.get("/", response_model=List[TransactionInDB])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    transactions = get_transactions(db, skip=skip, limit=limit)
    return transactions

# get all transactions by date range, with page and limit
@router.get("/getByDateRange", response_model=List[TransactionInDB])
def read_transactions_by_date_range(start_date: str, end_date: str, page: int = 0, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    transactions = get_transactions_by_date_range(db, start_date=start_date, end_date=end_date, page=page)
    return transactions

@router.get("/{transaction_id}", response_model=TransactionInDB)
def read_transaction(transaction_id: int, db: Session = Depends(get_user_db)):
    db_transaction = get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.put("/{transaction_id}", response_model=TransactionInDB)
def update_transaction_item(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_user_db)):
    updated_transaction = update_transaction(db, transaction_id, transaction)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction

@router.delete("/{transaction_id}")
def delete_transaction_item(transaction_id: int, db: Session = Depends(get_user_db)):
    deleted = delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}

@router.post("/preview")
async def preview_transactions_file(file: UploadFile = File(...), id: str = Form(...), db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    contents = await file.read()
    try:
        transactions = preview_transactions(contents, int(id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return transactions

@router.post("/upload")
async def upload_transactions_file(file: UploadFile = File(...), id: str = Form(...), db: Session = Depends(get_user_db), current_user: UserInDB = Depends(get_current_user)):
    contents = await file.read()
    try:
        upload_transactions(db, contents, file, int(id), current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Transactions uploaded successfully"}

"""create endpoint that dates date range for endpoint called analyze-duplicates"""
@router.get("/getByDateRangeForDuplicates/{start_date}/{end_date}", response_model=List[TransactionDuplicate])
def read_transactions_by_date_range_for_duplicates(start_date: str, end_date: str, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    transactions = get_transactions_by_date_range_for_duplicates(db, start_date=start_date, end_date=end_date)
    return transactions


"""create endpoint get transactions for batch id"""
@router.get("/batch/{batch_id}", response_model=List[TransactionInDB])
def read_transactions_by_batch(batch_id: int, page: int, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    transactions = get_transactions_by_batch(db, batch_id=batch_id, page=page)
    return transactions

"""create endpoint to delete trnasactions by batch id"""
@router.delete("/batch/{batch_id}")
def delete_transactions_by_batch(batch_id: int, db: Session = Depends(get_user_db)):
    deleted = delete_transactions_by_batch(db, batch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return {"detail": "Transactions deleted successfully"}