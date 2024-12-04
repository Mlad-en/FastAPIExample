from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.db.conn import DBConfig
from src.db.models import Base


engine = create_engine(DBConfig().get_url())
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def create_all_tables():
    Base.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
