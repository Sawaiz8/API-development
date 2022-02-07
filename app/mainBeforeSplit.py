from fastapi import HTTPException
from fastapi import FastAPI
'from fastapi.params import Body' #fast api params coming from frontend

from fastapi import Response #Use response 
from fastapi import status #get a list of statuses

from . import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import engine, get_db

from . import schemas
from typing import List

from . import utils


#binding our models to the engine of our selected database
#and so that we can make queries to it. (IMP)
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse) 
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #unpacking fields like this is inefficient so we convert pydantic model into a dict and 
    #unpack automatically using **post.dict()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #alternative to return statement
    return new_post

'''
#Have to use list from typing to send multiple responses 
@app.get("/posts", response_model = List[schemas.PostResponse]) 
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if posts == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return posts 
'''
@app.get("/posts/{id}", response_model = schemas.PostResponse) #{id} path parameter
def get_post(id: int, db: Session = Depends(get_db)):
    #filter = where
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post 


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db: Session = Depends(get_db) ):
    #we first have to check for exitence of id
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    #we delete using delete instead of first or all
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session= False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    updated_post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return updated_post_query.first()

@app.post("/users", status_code= status.HTTP_201_CREATED, response_model = schemas.UserCreateResponse)
def create_user(userInfo: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hasher(userInfo.password)
    userInfo.password = hashed_password
    new_user = models.User(**userInfo.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model = schemas.UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_retrieved = db.query(models.User).filter(models.User.id == id).first()
    if not user_retrieved:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"User with id: {id} does not exist")
    return user_retrieved
                