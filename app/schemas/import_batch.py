"""create these schemas in ImportBatchCreate, ImportBatchUpdate, ImportBatchInDB"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import UserBase


class ImportBatchBase(BaseModel):
    imported_at: datetime = datetime.now()
    source: str
    file_name: str
    user_id: int
    user: Optional[UserBase] = None

    class Config:
        orm_mode = True

class ImportBatchBaseCreate(ImportBatchBase):
    pass

class ImportBatchBaseUpdate(ImportBatchBase):
    pass

class ImportBatchBaseInDB(ImportBatchBase):
    id: int

    class Config:
        orm_mode = True
