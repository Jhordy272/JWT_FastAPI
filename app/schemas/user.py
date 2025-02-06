from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True