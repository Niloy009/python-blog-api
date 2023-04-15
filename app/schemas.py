from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    # post_id: int
    title: str
    content: str
    published: bool= True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
   pass

class ResponsePost(PostBase):
    post_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
     email: EmailStr
     password: str
     
class UserCreate(UserBase):
    pass

class ResponseUser(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str
    