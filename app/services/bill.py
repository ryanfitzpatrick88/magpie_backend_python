from sqlalchemy.orm import Session
from app.db.models.bill import Bill
from app.schemas.bill import BillCreate, BillUpdate


def create_bill(db: Session, bill: BillCreate):
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def get_bills(db: Session):
    return db.query(Bill).all()


def get_bill(db: Session, bill_id: int):
    return db.query(Bill).filter(Bill.id == bill_id).first()


def update_bill(db: Session, bill_id: int, bill: BillUpdate):
    db_bill = get_bill(db, bill_id)
    if db_bill is None:
        return None
    for key, value in bill.dict().items():
        setattr(db_bill, key, value)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def delete_bill(db: Session, bill_id: int):
    db_bill = get_bill(db, bill_id)
    if db_bill is None:
        return None
    db.delete(db_bill)
    db.commit()
    return db_bill
