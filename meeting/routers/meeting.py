from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session


router = APIRouter()
get_db=database.get_db



@router.get("/meeting", response_model=List[schemas.ShowMeeting], tags=["meetings"])
def all(db: Session = Depends(database.get_db)):
    meetings = db.query(models.Meeting).all()
    return meetings


@router.post("/meeting", status_code=status.HTTP_201_CREATED, tags=["meetings"])
def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    # return db
    new_meeting = models.Meeting(title=request.title, body=request.body, user_id=1)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


@router.delete("/meeting/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["meetings"])
def destroy(id, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")
    meeting.delete(synchronize_session=False)
    db.commit()
    return "meeting deleted"


@router.put("/meeting/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["meetings"])
def update(id, request: schemas.Meeting, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")    
    meeting.update(request.dict())
    db.commit()
    return "updated"



@router.get("/meeting/{id}", status_code=200, response_model=schemas.ShowMeeting, tags=["meetings"])
def show(id, db: Session = Depends(get_db)):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting with id {id} is not avaliable",
        )

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return{"detail":f"Meeting with id {id} is not avaliable"}
    return meeting