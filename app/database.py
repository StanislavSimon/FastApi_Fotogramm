from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SessionType
from fastapi import Depends

DATABASE_URL = "sqlite:///./photogram.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()


def get_db() -> SessionType:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
