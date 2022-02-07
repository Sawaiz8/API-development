from fastapi import HTTPException
from fastapi import FastAPI
'from fastapi.params import Body' #fast api params coming from frontend

from pydantic import BaseModel #Used for data validation
from typing import Optional

from fastapi import Response #Use response 
from fastapi import status #get a list of statuses

import psycopg2
from psycopg2.extras import RealDictCursor
import time

class PostFormat(BaseModel):  #pydantic model datatype is different: you can convert using pydantic model.datatype
    title : str
    content : str
    published : bool = True #Default value 
    rating: Optional[int] = None

#doesn't work for param variables
'''
class IdFormatCheck(BaseModel):
    id : int
'''
while True:
    try: 
        # We have to use real dict cursor because this library doesn't tell us the column name 
        # when we are querying information and this allows us to do
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi database', 
                                user = 'postgres', password = 'strong1,', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("successfull connection to db")
        break
    except Exception as error:
        print(error)
        time.sleep(2)

app = FastAPI()

'''
@app.get("/")
def root():
    return {"message": "Hello World"} 

@app.get("/posts")
def get_posts():
    return {"data": "This is my posts"}

#Without pydantic

@app.post("/createposts")
def create_posts(payload: PostFormat = Body(...)):
    #extract everything is store it to the payload variable
    return {"new_post": f"title {payload['title']} content: {payload['content']}"} #return automatically converts it to JSON
'''

'''
@app.post("/posts") #call it just posts. All functionality related to posts should be like this
def create_posts(new_post: PostFormat):
    #change PostFormat 
    new_post = new_post.dict()
    return {"new_post": f"title {new_post['title']} content: {new_post['content']}"} #return automatically converts it to JSON
'''
#using postgress commands for the code
@app.post("/posts") #call it just posts. All functionality related to posts should be like this
def create_posts(new_post: PostFormat):
    #use %s method not f string
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                    (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()

    #committ pushes the changes into the database
    conn.commit()

    return {"data": new_post} #return automatically converts it to JSON

'''
#We manipulate the response
@app.get("/posts/{id}") #{id} path parameter
def get_posts(id: int, response: Response): 
    #:int Validation to check id can be properly converted into an integer
    #I used pydantic but doesn't exactly work on path parameters 
    found = False
    if not found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f "post with id: {id} was not found"}

    return {"post_detail": f"stuff {id}" }
'''

'''
#simpler way is to raise exceptions
@app.get("/posts/{id}") #{id} path parameter
def get_posts(id: int, response: Response): 
    found = False
    if not found:
        #give status code and error. Now we don't need response
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_detail": f"stuff {id}" }
'''

#Using postgress and get posts
@app.get("/posts/{id}") #{id} path parameter
def get_posts(id: int):
    #We don't use an f string here since that method doesn't automatically check for SQL injections
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #fetch one is stops after first match, fetchall gets us all
    posts = cursor.fetchone()
    if posts == None :
        #give status code and error. Now we don't need response
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_detail": f"stuff {id}" }


#Delete and update weren't seperated when using postgres


#Change the DEFAULT STATUS CODE we use when we delete something
#You send 204 when you don't want data to be sent back after deletion
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_posts(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        #give status code and error. Now we don't need response
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
#we want the updation to follow the same schema
def update_posts(id:int, post:PostFormat):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                    (post.title, post.content, post.published, id))
    updated_post  = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        #give status code and error. Now we don't need response
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"message": "Post updated"}

