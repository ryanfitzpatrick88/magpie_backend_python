from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel
from .user import User

class ImportBatch(BaseModel):
    __tablename__ = "import_batches"

    imported_at = Column(DateTime, nullable=False)
    source = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
