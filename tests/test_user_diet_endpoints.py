from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def test_assign_diet_to_user_endpoint():
    user_response = client.post(
        "/api/users/",
        json={
            "username": "endpointuser",
            "email": "endpoint@example.com",
            "password": "123456"
        }
    )
    diet_response = client.post(
        "/api/diets/",
        json={
            "name": "Keto",
            "description": "Low carb diet"
        }
    )

    user_id = user_response.json()["id"]
    diet_id = diet_response.json()["id"]

    response = client.put(f"/api/users/{user_id}/diets/{diet_id}")

    assert response.status_code == 200
    assert response.json()["user_id"] == user_id


def test_list_user_diets_endpoint():
    user_response = client.post(
        "/api/users/",
        json={
            "username": "listuser",
            "email": "list@example.com",
            "password": "123456"
        }
    )
    diet_response = client.post(
        "/api/diets/",
        json={
            "name": "Mediterranean",
            "description": "Balanced diet"
        }
    )

    user_id = user_response.json()["id"]
    diet_id = diet_response.json()["id"]

    client.put(f"/api/users/{user_id}/diets/{diet_id}")
    response = client.get(f"/api/users/{user_id}/diets")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == user_id


def test_unassign_diet_endpoint():
    user_response = client.post(
        "/api/users/",
        json={
            "username": "removeuser",
            "email": "remove@example.com",
            "password": "123456"
        }
    )
    diet_response = client.post(
        "/api/diets/",
        json={
            "name": "Vegan",
            "description": "Plant-based diet"
        }
    )

    user_id = user_response.json()["id"]
    diet_id = diet_response.json()["id"]

    client.put(f"/api/users/{user_id}/diets/{diet_id}")
    response = client.delete(f"/api/users/{user_id}/diets/{diet_id}")

    assert response.status_code == 200
    assert response.json()["user_id"] is None


def test_assign_diet_user_not_found_endpoint():
    diet_response = client.post(
        "/api/diets/",
        json={
            "name": "Dash",
            "description": "Low sodium diet"
        }
    )
    diet_id = diet_response.json()["id"]

    response = client.put(f"/api/users/9999/diets/{diet_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_assign_diet_not_found_endpoint():
    user_response = client.post(
        "/api/users/",
        json={
            "username": "ghost",
            "email": "ghost@example.com",
            "password": "123456"
        }
    )
    user_id = user_response.json()["id"]

    response = client.put(f"/api/users/{user_id}/diets/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Diet not found"