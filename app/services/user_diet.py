from sqlalchemy.orm import Session

from app.models.diet import Diet
from app.models.user import User


def get_user_diets(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    return db.query(Diet).filter(Diet.user_id == user_id).all()


def assign_diet_to_user(db: Session, user_id: int, diet_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None, "user_not_found"

    diet = db.query(Diet).filter(Diet.id == diet_id).first()
    if not diet:
        return None, "diet_not_found"

    diet.user_id = user_id
    db.commit()
    db.refresh(diet)
    return diet, None


def unassign_diet_from_user(db: Session, user_id: int, diet_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None, "user_not_found"

    diet = db.query(Diet).filter(Diet.id == diet_id).first()
    if not diet:
        return None, "diet_not_found"

    if diet.user_id != user_id:
        return None, "diet_not_assigned_to_user"

    diet.user_id = None
    db.commit()
    db.refresh(diet)
    return diet, None