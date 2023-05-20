from sqlalchemy import Column, Integer, String, Numeric, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from enum import Enum as PyEnum

class Frequency(PyEnum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"

class Bill(BaseModel):
    __tablename__ = "bills"

    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    frequency = Column(Enum(Frequency), nullable=False)
    merchant_id = Column(Integer, ForeignKey('merchants.id'), nullable=True)

    merchant = relationship('Merchant', backref='bills')

