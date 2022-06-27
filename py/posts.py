from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    id: UUID4


class PostInDBBase(PostBase):
    id: UUID4

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    id: Optional[UUID4] = None


class PostInDB(PostInDBBase):
    pass
