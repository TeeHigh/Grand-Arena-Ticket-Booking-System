import pytest
from app.db.test_session import engine, TestingSessionLocal
from app.db.base import Base
from fastapi.testclient import TestClient
from app.main import app
from app.db.deps import get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)
