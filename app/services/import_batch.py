"""Create all the functions needed for CRUD operations using SQL ALchemy models"""
from sqlalchemy.orm import Session
from app.db.models import ImportBatch, User
from app.schemas.import_batch import ImportBatchBaseCreate, ImportBatchBaseUpdate, ImportBatchBaseInDB

"""create a new import_batch"""
def create_import_batch(db: Session, import_batch: ImportBatchBaseCreate):
    db_import_batch = ImportBatch(**import_batch.dict(exclude={"user"}))
    db.add(db_import_batch)
    db.commit()
    db.refresh(db_import_batch)
    return db_import_batch

"""get all import_batchs"""
def get_import_batchs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ImportBatch).offset(skip).limit(limit).all()

"""get a specific import_batch"""
def get_import_batch(db: Session, import_batch_id: int):
    return db.query(ImportBatch).filter(ImportBatch.id == import_batch_id).first()

"""update a specific import_batch"""
def update_import_batch(db: Session, import_batch_id: int, import_batch: ImportBatchBaseUpdate):
    db_import_batch = db.query(ImportBatch).filter(ImportBatch.id == import_batch_id).first()
    if db_import_batch is None:
        return None
    update_data = import_batch.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_import_batch, key, value)
    db.add(db_import_batch)
    db.commit()
    db.refresh(db_import_batch)
    return db_import_batch

"""delete a specific import_batch"""
def delete_import_batch(db: Session, import_batch_id: int):
    db_import_batch = db.query(ImportBatch).filter(ImportBatch.id == import_batch_id).first()
    if db_import_batch is None:
        return None
    db.delete(db_import_batch)
    db.commit()
    return db_import_batch

"""get all import_batchs for a specific user"""
def get_import_batchs_by_user(db: Session, user_id: int):
    return db.query(ImportBatch).filter(ImportBatch.user_id == user_id).all()

"""get a specific import_batch for a specific user"""
def get_import_batch_by_user(db: Session, import_batch_id: int, user_id: int):
    return db.query(ImportBatch).filter(ImportBatch.id == import_batch_id, ImportBatch.user_id == user_id).first()

"""update a specific import_batch for a specific user"""
def update_import_batch_by_user(db: Session, import_batch_id: int, import_batch: ImportBatchBaseUpdate, user_id: int):
    db_import_batch = db.query(ImportBatch).filter(ImportBatch.id == import_batch_id, ImportBatch.user_id == user_id).first()
    if db_import_batch is None:
        return None
    update_data = import_batch.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_import_batch, key, value)
    db.add(db_import_batch)
    db.commit()
    db.refresh(db_import_batch)
    return db_import_batch

"""delete a specific import_batch for a specific user"""
def delete_import_batch_by_user(db: Session, import_batch_id: int, user_id: int):
    db_import_batch = db.query(ImportBatch).filter(ImportBatch.id == import_batch_id, ImportBatch.user_id == user_id).first()
    if db_import_batch is None:
        return None
    db.delete(db_import_batch)
    db.commit()
    return db_import_batch



