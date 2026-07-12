from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:18820959483@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # same as connection

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) # now sessionlocal become a class not connection

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

