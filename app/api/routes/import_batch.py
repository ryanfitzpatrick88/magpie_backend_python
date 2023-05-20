from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.import_batch import ImportBatchBaseCreate, ImportBatchBaseUpdate, ImportBatchBaseInDB
from app.db.models.user import User
from app.services.import_batch import create_import_batch, get_import_batchs, get_import_batch, update_import_batch, \
    delete_import_batch
from app.dependencies.dependecies import get_current_user, get_user_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


"""give me all the endpoints for crud operations using the app.db.models.import_batch model"""
@router.post("/", response_model=ImportBatchBaseInDB)
def create_import_batch_item(import_batch: ImportBatchBaseCreate, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    return create_import_batch(db, import_batch)

@router.get("/", response_model=List[ImportBatchBaseInDB])
def read_import_batchs(skip: int = 0, limit: int = 100, db: Session = Depends(get_user_db), current_user: User = Depends(get_current_user)):
    import_batchs = get_import_batchs(db, skip=skip, limit=limit)
    return import_batchs

@router.get("/{import_batch_id}", response_model=ImportBatchBaseInDB)
def read_import_batch(import_batch_id: int, db: Session = Depends(get_user_db)):
    db_import_batch = get_import_batch(db, import_batch_id=import_batch_id)
    if db_import_batch is None:
        raise HTTPException(status_code=404, detail="ImportBatch not found")
    return db_import_batch

@router.put("/{import_batch_id}", response_model=ImportBatchBaseInDB)
def update_import_batch_item(import_batch_id: int, import_batch: ImportBatchBaseUpdate, db: Session = Depends(get_user_db)):
    updated_import_batch = update_import_batch(db, import_batch_id, import_batch)
    if updated_import_batch is None:
        raise HTTPException(status_code=404, detail="ImportBatch not found")
    return updated_import_batch

@router.delete("/{import_batch_id}")
def delete_import_batch_item(import_batch_id: int, db: Session = Depends(get_user_db)):
    deleted = delete_import_batch(db, import_batch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ImportBatch not found")
    return {"detail": "ImportBatch deleted successfully"}




