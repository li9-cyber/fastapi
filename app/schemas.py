from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Literal



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
    owner_id: int
    owner: UserOut



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


#### token schema ############

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None



class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]