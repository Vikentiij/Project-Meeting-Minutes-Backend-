from pydantic import BaseModel

class Meeting(BaseModel):
    title: str
    body: str

class ShowMeeting(BaseModel):
    title: str
    body: str                                 # class ShowMeeting(Meeting):        
    class Config():                      
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str