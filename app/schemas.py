from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserCreateResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True