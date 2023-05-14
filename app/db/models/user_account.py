from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship
from app.db.models.base import BaseModel

class UserAccount(BaseModel):
    __tablename__ = "user_accounts"

    database = Column(String)
    alias = Column(String)
    is_active = Column(Boolean, default=True)

