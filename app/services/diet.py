from sqlalchemy.orm import Session
from app.models.diet import Diet
from app.schemas.diet import DietCreate, DietUpdate

def get_diet(db: Session, diet_id: int):
    return db.query(Diet).filter(Diet.id == diet_id).first()

def get_diets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Diet).offset(skip).limit(limit).all()

def create_diet(db: Session, diet: DietCreate):
    db_diet = Diet(**diet.model_dump())
    db.add(db_diet)
    db.commit()
    db.refresh(db_diet)
    return db_diet

def update_diet(db: Session, diet_id: int, diet: DietUpdate):
    db_diet = db.query(Diet).filter(Diet.id == diet_id).first()
    if db_diet:
        for key, value in diet.model_dump().items():
            setattr(db_diet, key, value)
        db.commit()
        db.refresh(db_diet)
    return db_diet

def delete_diet(db: Session, diet_id: int):
    db_diet = db.query(Diet).filter(Diet.id == diet_id).first()
    if db_diet:
        db.delete(db_diet)
        db.commit()
    return db_diet