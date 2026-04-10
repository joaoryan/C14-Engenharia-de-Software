import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.schemas.diet import DietCreate
from app.schemas.user import UserCreate
from app.services.diet import create_diet
from app.services.user import create_user
from app.services.user_diet import (
    assign_diet_to_user,
    get_user_diets,
    unassign_diet_from_user,
)

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


def test_assign_diet_to_user_service(db_session):
    user = create_user(
        db_session,
        UserCreate(
            username="igor",
            email="igor@example.com",
            password="123456"
        )
    )
    diet = create_diet(
        db_session,
        DietCreate(
            name="Keto",
            description="Low carb diet"
        )
    )

    updated_diet, error = assign_diet_to_user(db_session, user.id, diet.id)

    assert error is None
    assert updated_diet.user_id == user.id


def test_get_user_diets_service(db_session):
    user = create_user(
        db_session,
        UserCreate(
            username="joao",
            email="joao@example.com",
            password="123456"
        )
    )

    diet1 = create_diet(
        db_session,
        DietCreate(
            name="Paleo",
            description="High protein diet"
        )
    )
    diet2 = create_diet(
        db_session,
        DietCreate(
            name="Mediterranean",
            description="Balanced diet"
        )
    )

    assign_diet_to_user(db_session, user.id, diet1.id)
    assign_diet_to_user(db_session, user.id, diet2.id)

    diets = get_user_diets(db_session, user.id)

    assert diets is not None
    assert len(diets) == 2
    assert diets[0].user_id == user.id
    assert diets[1].user_id == user.id


def test_unassign_diet_from_user_service(db_session):
    user = create_user(
        db_session,
        UserCreate(
            username="maria",
            email="maria@example.com",
            password="123456"
        )
    )
    diet = create_diet(
        db_session,
        DietCreate(
            name="Vegan",
            description="Plant-based diet"
        )
    )

    assign_diet_to_user(db_session, user.id, diet.id)
    updated_diet, error = unassign_diet_from_user(db_session, user.id, diet.id)

    assert error is None
    assert updated_diet.user_id is None


def test_assign_diet_user_not_found(db_session):
    diet = create_diet(
        db_session,
        DietCreate(
            name="Test",
            description="Diet test"
        )
    )

    updated_diet, error = assign_diet_to_user(db_session, 9999, diet.id)

    assert updated_diet is None
    assert error == "user_not_found"


def test_assign_diet_not_found(db_session):
    user = create_user(
        db_session,
        UserCreate(
            username="teste",
            email="teste@example.com",
            password="123456"
        )
    )

    updated_diet, error = assign_diet_to_user(db_session, user.id, 9999)

    assert updated_diet is None
    assert error == "diet_not_found"


def test_get_user_diets_user_not_found(db_session):
    diets = get_user_diets(db_session, 9999)
    assert diets is None


def test_unassign_diet_not_assigned_to_user(db_session):
    user = create_user(
        db_session,
        UserCreate(
            username="ana",
            email="ana@example.com",
            password="123456"
        )
    )
    diet = create_diet(
        db_session,
        DietCreate(
            name="Dash",
            description="Low sodium diet"
        )
    )

    updated_diet, error = unassign_diet_from_user(db_session, user.id, diet.id)

    assert updated_diet is None
    assert error == "diet_not_assigned_to_user"