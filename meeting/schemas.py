from typing import List
from pydantic import BaseModel

class MeetingBase(BaseModel):
    title: str
    body: str

class Meeting(MeetingBase):
    class Config():                      
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    meetings: List[Meeting]= []     #List
    class Config():                      
        orm_mode = True


class ShowMeeting(BaseModel):
    title: str
    body: str
    creator: ShowUser                                 # class ShowMeeting(Meeting):        
    class Config():                      
        orm_mode = True
    