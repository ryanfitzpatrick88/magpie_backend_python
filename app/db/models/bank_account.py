from sqlalchemy import Column, Integer, String, Numeric, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from enum import Enum as PyEnum

class AccountType(PyEnum):
    CHEQUING = "CHEQUING"
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    CREDIT_CARD = "CREDIT_CARD"
    LOAN = "LOAN"
    INVESTMENT = "INVESTMENT"


class BankAccount(BaseModel):
    __tablename__ = "bank_accounts"

    account_name = Column(String(255), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    bank_name = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)  # Assuming ISO 4217 currency codes

