from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
import time
from .config import settings
from sqlalchemy.engine import URL




is_cloud_sql = settings.database_hostname.startswith("/cloudsql/")

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_username,
    password=settings.database_password,
    host=None if is_cloud_sql else settings.database_hostname,
    port=None if is_cloud_sql else int(settings.database_port),
    database=settings.database_name,
    query={"host": settings.database_hostname} if is_cloud_sql else {},
)

engine = create_engine(SQLALCHEMY_DATABASE_URL) # same as connection

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) # now sessionlocal become a class not connection

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try: 
#         connection = psycopg.connect(host = 'localhost', dbname = 'fastapi', 
#                                     user = 'postgres', password = '18820959483',
#                                     row_factory = dict_row)
#         cursor = connection.cursor()
#         print('Database connection was succesfull!')
#         break
#     except Exception as error:
#         print(f'Connecting to database failed\nError: {error}')
#         time.sleep(10)