from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str
    colorCode: Optional[str] = None
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True
