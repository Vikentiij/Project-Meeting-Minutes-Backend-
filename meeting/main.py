from turtle import title
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

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


@app.get("/meeting")
def all(db: Session = Depends(get_db)):
    meetings = db.query(models.Meeting).all()
    return meetings


@app.get("/meeting/{id}", status_code=200)
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
