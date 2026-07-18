from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published: bool

class Response(PostBase):
    id: int
    created_at: datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class UserLogin(BaseModel):
    email: EmailStr
    password: str


