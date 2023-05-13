from datetime import date
from pydantic import BaseModel
from typing import Optional


class BudgetBase(BaseModel):
    name: str
    amount: float
    start_date: date
    end_date: date


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    name: Optional[str] = None
    amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class BudgetInDBBase(BudgetBase):
    id: int

    class Config:
        orm_mode = True


class BudgetInDB(BudgetInDBBase):
    pass
