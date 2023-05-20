from sqlalchemy.orm import Session
from app.db.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate, MerchantUpdate


def create_merchant(db: Session, merchant: MerchantCreate):
    db_merchant = Merchant(**merchant.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant


def get_merchants(db: Session):
    return db.query(Merchant).all()


def get_merchant(db: Session, merchant_id: int):
    return db.query(Merchant).filter(Merchant.id == merchant_id).first()


def update_merchant(db: Session, merchant_id: int, merchant: MerchantUpdate):
    db_merchant = get_merchant(db, merchant_id)
    if db_merchant is None:
        return None
    for key, value in merchant.dict().items():
        setattr(db_merchant, key, value)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant


def delete_merchant(db: Session, merchant_id: int):
    db_merchant = get_merchant(db, merchant_id)
    if db_merchant is None:
        return None
    db.delete(db_merchant)
    db.commit()
    return db_merchant
