from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.db.models.bill import Frequency


class BillBase(BaseModel):
    description: str
    amount: float
    due_date: date
    frequency: Frequency
    merchant_id: Optional[int] = None


class BillCreate(BillBase):
    pass


class BillUpdate(BillBase):
    pass


class BillInDB(BillBase):
    id: int

    class Config:
        orm_mode = True
