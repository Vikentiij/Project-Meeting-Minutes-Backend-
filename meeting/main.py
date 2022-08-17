from turtle import title
from fastapi import FastAPI, Depends, status
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app= FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.post("/meeting", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    #return db
    new_meeting = models.Meeting(title=request.title, body=request.body)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting

@app.get("/meeting")
def all(db: Session = Depends(get_db)):
    meetings = db.query(models.Meeting).all()
    return meetings

@app.get("/meeting/{id}")
def show(id, db: Session = Depends(get_db)):
    meeting = db.query(models.Meeting).filter(models.Meeting.id==id).first()
    return meeting