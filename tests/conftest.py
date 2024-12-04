from datetime import datetime

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

from src.db.models import Base
from main import app
from src.models.request import Entity


@pytest.fixture(scope="session")
def db_url() -> str:
    return "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session(db_url: str):
    engine = create_engine(
        db_url,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    yield session
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(db_session):
    database = db_session()
    yield database
    database.close()


@pytest.fixture(scope="session")
def test_api_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def request_entity():
    new_entity = Entity(
        case_date=datetime.now(),
        case_id="Neque porro quisquam est qui dolorem",
        name="TEST NAME",
    )
    return new_entity
