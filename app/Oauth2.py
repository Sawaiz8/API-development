from http.client import HTTPException
from jose import JWTError, jwt
from . import schemas
from datetime import datetime, timedelta
#Secret_Key
#Algorithm
#Experation time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from . import models
from .database import get_db

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/login')

SECRET_KEY = "arbitaryLongNumber"
Algorithm = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy() #Payload
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #Payload with time
    #Create access token
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = Algorithm)
    
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [Algorithm])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data

#We use this function to verify token and get user object from database
def get_current_user(token: str = Depends(Oauth2_scheme), 
                        db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", 
                                            headers = {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()


    return user


