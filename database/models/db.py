# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get('DB_URI2', None)

db_engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()
meta = Base.metadata

#Generates db session
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally: 
        db.close()

def get_engine():
    return db_engine
