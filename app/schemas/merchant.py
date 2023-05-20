from typing import Optional
from pydantic import BaseModel


class MerchantBase(BaseModel):
    name: str
    category_id: int


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(MerchantBase):
    pass


class MerchantInDB(MerchantBase):
    id: int

    class Config:
        orm_mode = True
