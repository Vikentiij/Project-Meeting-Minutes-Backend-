from turtle import title
from fastapi import FastAPI
from . import schemas

app= FastAPI()





@app.post("/meeting")
def create(request: schemas.Meeting):
    return request