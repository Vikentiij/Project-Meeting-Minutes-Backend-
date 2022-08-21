from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session


router = APIRouter(
prefix= "/meeting",
tags=["meetings"]

)
get_db=database.get_db



@router.get("/", response_model=List[schemas.ShowMeeting])
def all(db: Session = Depends(database.get_db)):
    meetings = db.query(models.Meeting).all()
    return meetings


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    # return db
    new_meeting = models.Meeting(title=request.title, body=request.body, user_id=1)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")
    meeting.delete(synchronize_session=False)
    db.commit()
    return "meeting deleted"


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Meeting, db: Session = Depends(get_db)):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")    
    meeting.update(request.dict())
    db.commit()
    return "updated"



@router.get("/{id}", status_code=200, response_model=schemas.ShowMeeting)
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