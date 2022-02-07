from fastapi import HTTPException
from fastapi import FastAPI
'from fastapi.params import Body' #fast api params coming from frontend

from fastapi import Response #Use response 
from fastapi import status #get a list of statuses

from .. import models
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import engine, get_db

from .. import schemas
from typing import List

from .. import utils

from fastapi import APIRouter

router = APIRouter(prefix = "/users",
                    tags = ["Users"])

models.Base.metadata.create_all(bind = engine)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserCreateResponse)
def create_user(userInfo: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hasher(userInfo.password)
    userInfo.password = hashed_password
    new_user = models.User(**userInfo.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model = schemas.UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_retrieved = db.query(models.User).filter(models.User.id == id).first()
    if not user_retrieved:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist")
    return user_retrieved

