import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pydantic import ValidationError

from main import app
from app.db.base import Base
from app.db.session import get_db
from app.services.user import create_user, get_user, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user_service(db_session):
    user_data = UserCreate(username="serviceuser", email="service@example.com", password="password123")
    user = create_user(db_session, user_data)
    assert user.username == "serviceuser"
    assert user.email == "service@example.com"

def test_get_user_service(db_session):
    user_data = UserCreate(username="getuser", email="get@example.com", password="password123")
    user = create_user(db_session, user_data)
    fetched_user = get_user(db_session, user.id)
    assert fetched_user.id == user.id
    assert fetched_user.username == "getuser"

def test_update_user_service(db_session):
    user_data = UserCreate(username="updateuser", email="update@example.com", password="password123")
    user = create_user(db_session, user_data)
    update_data = UserUpdate(username="updateduser", email="update@example.com")
    updated_user = update_user(db_session, user.id, update_data)
    assert updated_user.username == "updateduser"

def test_delete_user_service(db_session):
    user_data = UserCreate(username="deleteuser", email="delete@example.com", password="password123")
    user = create_user(db_session, user_data)
    deleted_user = delete_user(db_session, user.id)
    assert deleted_user.username == "deleteuser"
    assert get_user(db_session, user.id) is None

def test_get_user_not_found(db_session):
    # ID inexistente
    fetched_user = get_user(db_session, 9999)
    assert fetched_user is None

def test_update_user_not_found(db_session):
    update_data = UserUpdate(username="ghost_user")
    updated_user = update_user(db_session, 9999, update_data)
    assert updated_user is None

def test_delete_user_not_found(db_session):
    deleted_user = delete_user(db_session, 9999)
    assert deleted_user is None

def test_user_create_missing_fields():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="incompleteuser")
    
    errors = exc_info.value.errors()
    failed_fields = [error["loc"][0] for error in errors]
    assert "email" in failed_fields
    assert "password" in failed_fields

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="bademailuser", 
            email="isso-nao-e-um-email", 
            password="password123"
        )

def test_user_update_empty_data():
    update_data = UserUpdate()
    assert update_data.dict(exclude_unset=True) == {}