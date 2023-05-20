from datetime import date
from pydantic import BaseModel
from typing import Optional
from app.schemas.category import CategoryBase


class BudgetBase(BaseModel):
    name: str
    amount: float
    start_date: date
    end_date: date
    category_id: int
    category: Optional[CategoryBase] = None


class BudgetCreate(BaseModel):
    name: str
    amount: float
    start_date: date
    end_date: date
    category_id: int


class BudgetUpdate(BaseModel):
    name: str
    amount: float
    start_date: date
    end_date: date
    category_id: int


class BudgetInDBBase(BudgetBase):
    id: int

    class Config:
        orm_mode = True


class BudgetInDB(BudgetInDBBase):
    pass
