from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Budget(BaseModel):
    __tablename__ = "budgets"

    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # This line will let you access the Category object associated with a Budget via the 'category' attribute
    category = relationship('Category', backref='budgets')
