# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqldb://root:ArgPepLoc546&@localhost/ephm3ralmusic"

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