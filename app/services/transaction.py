from datetime import datetime
from io import StringIO
import csv
from sqlalchemy.orm import Session
from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionImport
from app.schemas.import_batch import ImportBatchBaseCreate
from app.api.routes.import_batch import create_import_batch
from app.schemas.user import UserBase


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction is None:
        return None
    for var, value in vars(transaction).items():
        setattr(db_transaction, var, value) if value else None
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction is None:
        return False
    db.delete(db_transaction)
    db.commit()
    return True

"""get_transactions_by_batch"""
def get_transactions_by_batch(db: Session, batch_id: int):
    return db.query(Transaction).filter(Transaction.batch_id == batch_id).all()

"""delete_transactions_by_batch"""
def delete_transactions_by_batch(db: Session, batch_id: int):
    db_transactions = get_transactions_by_batch(db, batch_id)
    if db_transactions is None:
        return False
    for transaction in db_transactions:
        db.delete(transaction)
    db.commit()
    return True

def preview_transactions(file_contents: bytes):
    transactions = []
    file_str = file_contents.decode()
    reader = csv.DictReader(StringIO(file_str))

    for row in reader:
        transaction_raw = TransactionImport(**row)
        transaction_data = TransactionCreate(
            description=transaction_raw.Description,
            amount=transaction_raw.Amount.replace('$', '', len(transaction_raw.Amount)),
            date=transaction_raw.Date,
            batch_id=0
        )
        transactions.append(transaction_data)

    return transactions


def upload_transactions(db: Session, file_contents: bytes, file, current_user:UserBase):
    file_str = file_contents.decode()
    reader = csv.DictReader(StringIO(file_str))

    batch = ImportBatchBaseCreate(
        imported_at = datetime.now(),
        source = "csv",
        file_name = file.filename,
        user_id = current_user.id
    )
    batch = create_import_batch(db, batch)

    for row in reader:
        transaction_raw = TransactionImport(**row)
        transaction_data = TransactionCreate(
            description=transaction_raw.Description,
            amount=transaction_raw.Amount.replace('$','',len(transaction_raw.Amount)),
            date=transaction_raw.Date,
            batch = batch,
            batch_id = batch.id
        )
        create_transaction(db, transaction_data)
