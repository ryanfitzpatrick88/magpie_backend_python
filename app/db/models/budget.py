from sqlalchemy import Column, Integer, String, Numeric, Date
from .base import BaseModel

class Budget(BaseModel):
    __tablename__ = "budgets"

    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
