import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pydantic import ValidationError

from app.db.base import Base
from app.db.session import get_db
from app.services.diet import create_diet, get_diet, update_diet, delete_diet
from app.schemas.diet import DietCreate, DietUpdate

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

def test_create_diet_service(db_session):
    diet_data = DietCreate(name="Keto", description="Low carb diet")
    diet = create_diet(db_session, diet_data)
    assert diet.name == "Keto"
    assert diet.description == "Low carb diet"

def test_get_diet_service(db_session):
    diet_data = DietCreate(name="Paleo", description="High protein diet")
    diet = create_diet(db_session, diet_data)
    fetched_diet = get_diet(db_session, diet.id)
    assert fetched_diet.id == diet.id
    assert fetched_diet.name == "Paleo"

def test_update_diet_service(db_session):
    diet_data = DietCreate(name="Mediterranean", description="Balanced diet")
    diet = create_diet(db_session, diet_data)
    update_data = DietUpdate(name="Updated Mediterranean", description="Updated description")
    updated_diet = update_diet(db_session, diet.id, update_data)
    assert updated_diet.name == "Updated Mediterranean"

def test_delete_diet_service(db_session):
    diet_data = DietCreate(name="Vegan", description="Plant-based diet")
    diet = create_diet(db_session, diet_data)
    deleted_diet = delete_diet(db_session, diet.id)
    assert deleted_diet.name == "Vegan"
    assert get_diet(db_session, diet.id) is None

def test_get_diet_not_found(db_session):
    fetched_diet = get_diet(db_session, 9999)
    assert fetched_diet is None

def test_update_diet_not_found(db_session):
    update_data = DietUpdate(name="Nonexistent Diet", description="")
    updated_diet = update_diet(db_session, 9999, update_data)
    assert updated_diet is None

def test_delete_diet_not_found(db_session):
    deleted_diet = delete_diet(db_session, 9999)
    assert deleted_diet is None

def test_diet_create_missing_fields():
    with pytest.raises(ValidationError) as exc_info:
        DietCreate(name="Incomplete Diet")

    errors = exc_info.value.errors()
    failed_fields = [error["loc"][0] for error in errors]
    assert "description" in failed_fields