from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import PostgresDsn
'from fastapi.params import Body' #fast api params coming from frontend

from fastapi import Response #Use response 
from fastapi import status #get a list of statuses

from .. import models
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import engine, get_db

from .. import schemas
from typing import List

from fastapi import APIRouter

from .. import Oauth2

#We can use routers to define prefixes for the path so that we don't type it all togather 
router = APIRouter(prefix = "/posts",
                    tags = ["Posts"])

models.Base.metadata.create_all(bind = engine)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse) 
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user  = Depends(Oauth2.get_current_user)):
    #Adding this dependancy connects to authenticated user_id. If not authenticated then it won't work
    #I don't think user is int anymore but the code works finee
 
    print(current_user.email)
    print(current_user.id)

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #unpacking fields like this is inefficient so we convert pydantic model into a dict and 
    #unpack automatically using **post.dict()
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #alternative to return statement
    return new_post

@router.get("/{id}", response_model = schemas.PostResponse) #{id} path parameter
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int  = Depends(Oauth2.get_current_user)):
    #filter = where
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id:int, db: Session = Depends(get_db) , 
                    current_user = Depends(Oauth2.get_current_user)):
#Adding this dependancy connects to authenticated user_id. If not authenticated then it won't work

    #we first have to check for exitence of id
    delete_post = db.query(models.Post).filter(models.Post.id == id).first()
    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requrested action")
    
    #we delete using delete instead of first or all
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session= False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), 
                    current_user: int  = Depends(Oauth2.get_current_user)):
#Adding this dependancy connects to authenticated user_id. If not authenticated then it won't work
    
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requrested action")
    
    updated_post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return updated_post_query.first()

#We don't restrict our posts to specific users
@router.get("/", response_model = List[schemas.PostResponse]) 
def get_posts(db: Session = Depends(get_db)):
    #the type you put here doesn't matter for some reason
    #We filter the ids here.
    posts = db.query(models.Post).all()

    if posts == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    return posts 