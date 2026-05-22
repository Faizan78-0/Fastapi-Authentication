import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user(test_client):
    response = test_client.post("/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201, response.text
    return {"email": "test@gmail.com", "password": "123456"}

@pytest.fixture
def admin_user(test_client):
    
    test_client.post("/auth/register",
        json={
            "email": "admin@gmail.com",
            "password": "123456"
        }
    )

    response = test_client.post("/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def token(test_client, test_user):
    response = test_client.post("/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data, data
    return data["access_token"]


@pytest.fixture
def authorized_client(test_client, token):

    test_client.headers = {"Authorization": f"Bearer {token}"}

    yield test_client