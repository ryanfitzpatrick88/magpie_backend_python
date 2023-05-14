from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.schemas.import_batch import ImportBatchBase

class TransactionImport(BaseModel):
    Date: date = Field(..., alias="Date")
    Description: str = Field(..., alias="Description")
    Reference: Optional[str] = Field(None, alias="Reference")
    Amount: str = Field(..., alias="Amount")
    Balance: str = Field(..., alias="Balance")

    class Config:
        allow_population_by_field_name = True

    @validator('Date', pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, '%d%b%Y')  # Parses date in the format "11May2023"


class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    batch_id: int
    category: Optional[str] = None
    batch: Optional[ImportBatchBase] = None

    class Config:
        orm_mode = True # Pydantic will read the data even if it is not a dict

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: int

    class Config:
        orm_mode = True

class TransactionDuplicate(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    transactions: List[TransactionInDB]

