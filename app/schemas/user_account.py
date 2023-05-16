from pydantic import BaseModel

class UserAccount(BaseModel):
    database: str
    alias: str
    is_active: bool

class UserAccountCreate(UserAccount):
    pass

class UserAccountUpdate(UserAccount):
    pass

class UserAccountInDB(UserAccount):
    id: int

    # Add other fields specific to UserAccount in the database

    class Config:
        orm_mode = True
