from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db import constant as con
import os

DATABASE_URL_LOCAL=con.DATABASE_URL_LOCAL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    DATABASE_URL_LOCAL
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

Base = declarative_base()
