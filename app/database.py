#for most applciation we just copy past this
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:strong1,@localhost/fastapi database"

#engine establishes connection
engine = create_engine(SQLALCHEMY_DATABASE_URL) 

#When we want to communicate thorugh session
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind =engine)

#all the models defined will be extend this base class
Base = declarative_base() 

#dependancy to comunnicate with the database 
#whenever we get a request we will start a session then yield the result
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()