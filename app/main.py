from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine
from .database import get_db
from typing import List



models.Base.metadata.create_all(bind = engine)  #get the metadata in baseclass and then create table



app = FastAPI()



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




        
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy") 
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts")
def get_posts(db: Session = Depends(get_db), response_model=List[schemas.Response]):
    #cursor.execute('SELECT * FROM posts;')
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute('''
    #                 INSERT INTO posts 
    #                (title, content, published)
    #                VALUES (%s, %s, %s)
    #                RETURNING * 
    #                ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.Response)
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
    return post

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''
    #                 DELETE FROM posts
    #                WHERE id = %s
    #                RETURNING *;
    #                 ''', (id, ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Response)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute('''
    #                 UPDATE posts
    #                SET title = %s,
    #                     content = %s,
    #                     published = %s
    #                WHERE id = %s
    #                 RETURNING *;
    #                 ''', (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_get = updated_post.first()
    if post_get is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
    updated_post.update(post.model_dump())
    db.commit()
    db.refresh(post_get)
    return post_get





