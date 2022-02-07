
from tkinter import CASCADE
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text, null

from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts" #table name

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    #Server default to write default answers
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, 
                    server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
#We will import our models in the main file

    owner = relationship("User")
    #this line will automatically give us the relationship of user to us
    #from the post. 
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable = False, unique= True, primary_key= True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), 
                        nullable =False, server_default= text(('now()')))


