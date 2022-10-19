from datetime import datetime
from typing import Optional
from pydantic import BaseModel , EmailStr, conint

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class VoteOut(BaseModel):
    vote : int

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostwVote(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Token(BaseModel):
    token : str
    type : str

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id : int
    dir : conint(lt=2,ge=0)