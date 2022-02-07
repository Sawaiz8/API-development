from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from ..database import engine, get_db
from .. import schemas
from .. import models
from .. import utils
from .. import Oauth2

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags = ["Authentication"])

@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OauthpasswordRequestForm only uses username tag rather than email
    #user_credentials.username == email
    #In postman the data isn't coming in JSON format it will now come in form data
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                              detail = f"Invalid Credentials")

    #verify password using the utlity function we created with passlib Oauth  
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    #creating a token
    #we put other data like which frontend its going to etc
    access_token = Oauth2.create_access_token(data = {"user_id": user.id})

    #bearer token are configured at frontend
    return {"access_token": access_token, "token_type" : "bearer"}