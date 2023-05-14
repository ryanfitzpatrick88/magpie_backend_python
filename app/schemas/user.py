from pydantic import BaseModel, EmailStr
from app.schemas.user_account import UserAccount, UserAccountInDB
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool
    user_account: Optional[UserAccount] = None

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True
    user_account: UserAccount

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    user_account: Optional[UserAccountInDB] = None

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
