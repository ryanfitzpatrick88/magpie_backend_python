from typing import Optional
from pydantic import BaseModel

from app.schemas.category import CategoryBase, CategoryInDB


class MerchantBase(BaseModel):
    name: str
    category_id: int


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(MerchantBase):
    pass


class MerchantInDB(MerchantBase):
    id: int
    category: Optional[CategoryInDB] = None

    class Config:
        orm_mode = True
