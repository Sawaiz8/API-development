from datetime import datetime
from pydantic import BaseModel #Used for data validation
from typing import Optional

from pydantic import EmailStr #used for email validation

class UserCreate(BaseModel):
    email: EmailStr #Does it check whether it exists or not? or just format
    password: str

class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
         orm_mode = True

class UserGetResponse(UserCreateResponse):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



#i moved user related relationships above






class PostFormat(BaseModel):  #pydantic model datatype is different: you can convert using pydantic model.datatype
    title : str
    content : str
    published : bool = True #Default value   

'''
class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePost(BaseModel):
#If we remove other then user won't be able to update such posts
#    title: str
#   content: str
    published: bool 
'''

class PostCreate(PostFormat):
    #we can allow the user to give the owner_id 
    # but we didnt because it's not needed. The twitter knows
    # that you are the users.
    #It should it from authentication status
    pass

#do inheritance  
class PostResponse(PostFormat):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateResponse
    #this tells the pydantic model that the response data is in sqlachemy (ORM) format
    class Config:
         orm_mode = True

