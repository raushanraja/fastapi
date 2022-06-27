from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional
from .posts import Post

class UserBase(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    name: str
    username: str
    password: str

class UserUpdate(UserBase):
    id: UUID4

class UserInDBBase(UserBase):
    id: UUID4
    post: Optional[Post] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass