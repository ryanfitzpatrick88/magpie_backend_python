from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from app.schemas.bank_account import BankAccountBase, BankAccountInDB
from app.schemas.import_batch import ImportBatchBase, ImportBatchBaseInDB

"""
This class is used to parse the CSV file uploaded by the user.
"""
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
    batch: Optional[ImportBatchBase] = None
    bank_account_id: int
    bank_account: Optional[BankAccountBase] = None

    class Config:
        orm_mode = True # Pydantic will read the data even if it is not a dict

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: int
    bank_account: Optional[BankAccountInDB] = None
    batch: Optional[ImportBatchBaseInDB] = None

    class Config:
        orm_mode = True

class TransactionDuplicate(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    transactions: List[TransactionInDB]

