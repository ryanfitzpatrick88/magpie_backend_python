from datetime import datetime
from io import StringIO
import csv
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.models import User
from app.db.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionImport, TransactionDuplicate
from app.schemas.import_batch import ImportBatchBaseCreate
from app.api.routes.import_batch import create_import_batch
from app.schemas.user import UserBase, UserInDB


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

# get_transactions_by_date_range
def get_transactions_by_date_range(db: Session, start_date: str, end_date: str, page: int = 1, page_size: int = 10):
    transactions = db.query(Transaction).filter(and_(Transaction.date >= start_date, Transaction.date <= end_date))
    transactions = transactions.offset(page_size * (page - 1)).limit(page_size)
    return transactions.all()

def get_transactions_by_date_range_for_duplicates(db: Session, start_date: str, end_date: str):
    transactions = db.query(Transaction).filter(and_(Transaction.date >= start_date, Transaction.date <= end_date)).all()
    duplicates_dict = {}

    for transaction in transactions:
        key = (transaction.description, transaction.amount, transaction.date)
        if key not in duplicates_dict:
            duplicates_dict[key] = [transaction.id]
        else:
            duplicates_dict[key].append(transaction.id)

    # Filter out keys where there is only one transaction, as this means there are no duplicates
    duplicates_dict = {key: value for key, value in duplicates_dict.items() if len(value) > 1}

    # Create TransactionDuplicate objects for each duplicate
    duplicates = []
    for key, ids in duplicates_dict.items():
        duplicate_transactions = []
        for id in ids:
            # Retrieve the actual transaction object for each id
            transaction = db.query(Transaction).filter(Transaction.id == id).first()
            if transaction:
                duplicate_transactions.append(transaction)

        # Create a TransactionDuplicate object
        if duplicate_transactions:
            duplicate = TransactionDuplicate(
                description=key[0],
                amount=key[1],
                date=key[2],
                transactions=duplicate_transactions
            )
            duplicates.append(duplicate)

    return duplicates

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict(exclude={"batch", "bank_account"}))
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
def get_transactions_by_batch(db: Session, batch_id: int, page: int, page_size: int = 10):
    transactions = db.query(Transaction).filter(batch_id == Transaction.batch_id)
    transactions = transactions.offset(page_size * (page - 1)).limit(page_size)
    return transactions.all()

"""delete_transactions_by_batch"""
def delete_transactions_by_batch(db: Session, batch_id: int):
    db_transactions = get_transactions_by_batch(db, batch_id)
    if db_transactions is None:
        return False
    for transaction in db_transactions:
        db.delete(transaction)
    db.commit()
    return True

def preview_transactions(file_contents: bytes, bank_account_id: int):
    transactions = []
    file_str = file_contents.decode()
    reader = csv.DictReader(StringIO(file_str))

    for row in reader:
        transaction_raw = TransactionImport(**row)
        transaction_data = TransactionCreate(
            description=transaction_raw.Description,
            amount=transaction_raw.Amount.replace('$', '', len(transaction_raw.Amount)),
            date=transaction_raw.Date,
            batch_id=0,
            bank_account_id=bank_account_id
        )
        transactions.append(transaction_data)

    return transactions


def upload_transactions(db: Session, file_contents: bytes, file, bank_account_id: int, current_user: UserInDB):
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
            batch_id = batch.id,
            bank_account_id = bank_account_id
        )
        create_transaction(db, transaction_data)
