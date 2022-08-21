from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id =Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="meetings")


class User(Base):
    __tablename__ ="users"
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String)
    email = Column(String)
    password= Column(String)

    meetings= relationship("Meeting", back_populates="creator")