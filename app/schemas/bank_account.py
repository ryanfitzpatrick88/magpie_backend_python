from typing import Optional
from pydantic import BaseModel
from app.db.models.bank_account import AccountType


class BankAccountBase(BaseModel):
    account_name: str
    account_type: AccountType
    bank_name: str
    currency: str


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountUpdate(BankAccountBase):
    pass


class BankAccountInDB(BankAccountBase):
    id: int

    class Config:
        orm_mode = True
