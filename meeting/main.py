from fastapi import FastAPI, status, Request
from . import models
from .database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from .routers import meeting, user, authentication
#from passlib.context import CryptContext

app = FastAPI()

templates= Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(engine)


@app.get("/", status_code=status.HTTP_201_CREATED, tags=["home_page"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(authentication.router)
app.include_router(meeting.router)
app.include_router(user.router)


#def get_db():     # move to database.py
   # db = SessionLocal()
   # try:
    #    yield db
    #finally:
     #   db.close


#@app.post("/meeting", status_code=status.HTTP_201_CREATED, tags=["meetings"])
#def create(request: schemas.Meeting, db: Session = Depends(get_db)):
    # return db
    #new_meeting = models.Meeting(title=request.title, body=request.body, user_id=1)
    #db.add(new_meeting)
    #db.commit()
    #db.refresh(new_meeting)
    #return new_meeting




#@app.get("/meeting", response_model=List[schemas.ShowMeeting], tags=["meetings"])
#def all(db: Session = Depends(get_db)):
   # meetings = db.query(models.Meeting).all()
   # return meetings







#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  --- move to hashing.py



