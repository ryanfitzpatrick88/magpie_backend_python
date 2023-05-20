from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String)
    description = Column(String)
    colorCode = Column(String, nullable=True)
    icon = Column(String, nullable=True)

    def __init__(self, name, description, colorCode=None, icon=None):
        self.name = name
        self.description = description
        self.colorCode = colorCode
        self.icon = icon
