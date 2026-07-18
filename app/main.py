from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine
from .database import get_db
from .routers import post, user, auth





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




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
        

@app.get("/")
def root():
    return {"message": "Hello World"}

