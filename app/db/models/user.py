from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship
from app.db.models.base import BaseModel
from app.db.models.user_account import UserAccount

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_account_id = Column(Integer, ForeignKey('user_accounts.id'))

    user_account = relationship(UserAccount, uselist=False)

    @validates("email")
    def validate_email(cls, key, value):
        if not value:
            raise ValueError("Email is required")
        return value

    @validates("hashed_password")
    def validate_password(cls, key, value):
        if not value:
            raise ValueError("Password is required")
        return value
