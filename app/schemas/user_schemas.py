from typing import List, Optional
from pydantic import BaseModel,EmailStr,constr

class CreateAccount(BaseModel):
    name:str
    email:EmailStr
    password:str = constr(min_length=8)
    confirm_password: str

class Login(BaseModel):
    email:EmailStr
    password:str

class ShowUser(BaseModel):
    name:str
    email:EmailStr

    
    class Config:
        orm_mode: True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreateResponse(BaseModel):
    message: str
    user: ShowUser

