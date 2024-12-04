from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode= True

class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes=True