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
from .database import engine
from .database import get_db


models.Base.metadata.create_all(bind = engine)  #get the metadata in baseclass and then create table



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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
    posts = db.query(models.Post).all()
    return {"data:": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute('SELECT * FROM posts;')
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute('''
    #                 INSERT INTO posts 
    #                (title, content, published)
    #                VALUES (%s, %s, %s)
    #                RETURNING * 
    #                ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''
    #                 SELECT * FROM posts
    #                WHERE id = %s
    #                 ''', (id, ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
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



