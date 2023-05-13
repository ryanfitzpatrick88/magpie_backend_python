from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool
    database: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AccessToken(BaseModel):
    access_token: str

class LoginToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ValidateToken(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginForm(BaseModel):
    email: str
    password: str

class EmailSchema(BaseModel):
    email: str

class CheckEmailResponse(BaseModel):
    emailExists: bool