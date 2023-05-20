from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Transaction(BaseModel):
    __tablename__ = "transactions"

    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    batch_id = Column(Integer, ForeignKey('import_batches.id'))
    merchant_id = Column(Integer, ForeignKey('merchants.id'), nullable=True)
    bank_account_id = Column(Integer, ForeignKey('bank_accounts.id'))

    batch = relationship('ImportBatch', backref='transactions')
    merchant = relationship('Merchant', backref='transactions')
    bank_account = relationship('BankAccount', backref='transactions')