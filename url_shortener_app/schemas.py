'''
Your schema states what your API expects as a request body and what the client can expect in the response body. 
'''
from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str

class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        '''We tell pydantic with orm_mode = True to work with a database model.
        ORM = Object-Relational Mapping
        '''
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str