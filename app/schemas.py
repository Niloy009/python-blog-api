from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    post_id: int
    title: str
    content: str
    published: bool= True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
   pass

class ResponsePost(PostBase):
    # id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
     email: EmailStr
     password: str
     
class UserCreate(UserBase):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True