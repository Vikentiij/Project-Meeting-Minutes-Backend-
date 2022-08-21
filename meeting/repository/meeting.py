from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status




def get_all(db: Session):
    meetings = db.query(models.Meeting).all()
    return meetings



def create(request: schemas.Meeting, db:Session):
    new_meeting = models.Meeting(title=request.title, body=request.body, user_id=1)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


def destroy(id:int, db:Session):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")
    meeting.delete(synchronize_session=False)
    db.commit()
    return "meeting deleted"


def update(id:int, request: schemas.Meeting, db:Session):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")    
    meeting.update(request.dict())
    db.commit()
    return "updated"


def show(id:int, db:Session):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting with id {id} is not avaliable",
        )

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return{"detail":f"Meeting with id {id} is not avaliable"}
    return meeting
