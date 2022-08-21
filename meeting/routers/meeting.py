from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..repository import meeting


router = APIRouter(
prefix= "/meeting",
tags=["meetings"]

)
get_db=database.get_db



@router.get("/", response_model=List[schemas.ShowMeeting])
def all(db: Session = Depends(database.get_db)):
    return meeting.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    return meeting.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
   return meeting.destroy(id,db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Meeting, db: Session = Depends(get_db)):
    return meeting.update(id, request, db)



@router.get("/{id}", status_code=200, response_model=schemas.ShowMeeting)
def show(id:int, db: Session = Depends(get_db)):
    return meeting.show(id,db)