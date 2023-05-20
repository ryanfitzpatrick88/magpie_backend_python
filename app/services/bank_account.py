from sqlalchemy.orm import Session
from app.db.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate


def create_bank_account(db: Session, bank_account: BankAccountCreate):
    db_bank_account = BankAccount(**bank_account.dict())
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account


def get_bank_accounts(db: Session):
    return db.query(BankAccount).all()


def get_bank_account(db: Session, bank_account_id: int):
    return db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()


def update_bank_account(db: Session, bank_account_id: int, bank_account: BankAccountUpdate):
    db_bank_account = get_bank_account(db, bank_account_id)
    if db_bank_account is None:
        return None
    for key, value in bank_account.dict().items():
        setattr(db_bank_account, key, value)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account


def delete_bank_account(db: Session, bank_account_id: int):
    db_bank_account = get_bank_account(db, bank_account_id)
    if db_bank_account is None:
        return None
    db.delete(db_bank_account)
    db.commit()
    return db_bank_account
