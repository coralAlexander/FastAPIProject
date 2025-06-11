from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class Config:
    from_attributes = True  # для работы с ORM-моделями
