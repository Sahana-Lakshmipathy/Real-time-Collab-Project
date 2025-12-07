from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    id: str                 # you are using custom string IDs
    username: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    created_at: Optional[str]

    class Config:
        orm_mode = True
