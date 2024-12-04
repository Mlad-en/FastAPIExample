import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from src.db.models import Base
from src.db.session import get_db
from src.models.request import Entity


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def test_api_client(db_session) -> TestClient:
    def mock_conn():
        database = db_session()
        yield database
        database.close()

    client = TestClient(app)
    app.dependency_overrides[get_db] = mock_conn
    return client


@pytest.fixture(scope="function")
def request_entity():
    new_entity = Entity(
        case_date=datetime.now(),
        case_id="Neque porro quisquam est qui dolorem",
        name="TEST NAME",
    )
    return new_entity


@pytest.fixture(scope="function")
def request_entity_json(request_entity):
    return json.loads(request_entity.model_dump_json())
