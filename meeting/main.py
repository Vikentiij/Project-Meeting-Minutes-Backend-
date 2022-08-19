from turtle import title
from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
#from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.post("/meeting", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    # return db
    new_meeting = models.Meeting(title=request.title, body=request.body)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


@app.delete("/meeting/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")
    meeting.delete(synchronize_session=False)
    db.commit()
    return "meeting deleted"


@app.put("/meeting/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Meeting, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")    
    meeting.update(request.dict())
    db.commit()
    return "updated"


@app.get("/meeting", response_model=List[schemas.ShowMeeting])
def all(db: Session = Depends(get_db)):
    meetings = db.query(models.Meeting).all()
    return meetings


@app.get("/meeting/{id}", status_code=200, response_model=schemas.ShowMeeting)
def show(id, response: Response, db: Session = Depends(get_db)):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting with id {id} is not avaliable",
        )

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return{"detail":f"Meeting with id {id} is not avaliable"}
    return meeting




#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  --- move to hashing.py


@app.post("/user")
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    # hashedPassword = pwd_context.hash(request.password) ---- move to hashing.py
    new_user = models.User(name= request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))  #password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user