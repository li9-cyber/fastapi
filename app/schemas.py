from pydantic import BaseModel
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
