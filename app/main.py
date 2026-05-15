from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind = engine)  #get the metadata in baseclass and then create table

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try: 
        connection = psycopg.connect(host = 'localhost', dbname = 'fastapi', 
                                    user = 'postgres', password = '18820959483',
                                    row_factory = dict_row)
        cursor = connection.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as error:
        print(f'Connecting to database failed\nError: {error}')
        time.sleep(10)


class updatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

        
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy") 
def test_post(db: Session = Depends(get_db)):
    return {"status": "sucess"}


@app.get("/posts")
def get_posts():
    cursor.execute('''
                    SELECT * FROM posts;
                    ''')
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('''
                    INSERT INTO posts 
                   (title, content, published)
                   VALUES (%s, %s, %s)
                   RETURNING * 
                   ''', (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return{"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('''
                    SELECT * FROM posts
                   WHERE id = %s
                    ''', (id, ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute('''
                    DELETE FROM posts
                   WHERE id = %s
                   RETURNING *;
                    ''', (id, ))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    connection.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''
                    UPDATE posts
                   SET title = %s,
                        content = %s,
                        published = %s
                   WHERE id = %s
                    RETURNING *;
                    ''', (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")

    connection.commit()
    return {'data': updated_post}




