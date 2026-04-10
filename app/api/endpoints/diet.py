from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.diet import get_diet, get_diets, create_diet, update_diet, delete_diet
from app.schemas.diet import DietCreate, DietUpdate, DietResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[DietResponse])
def read_diets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_diets(db, skip=skip, limit=limit)

@router.get("/{diet_id}", response_model=DietResponse)
def read_diet(diet_id: int, db: Session = Depends(get_db)):
    db_diet = get_diet(db, diet_id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    return db_diet

@router.post("/", response_model=DietResponse)
def create_new_diet(diet: DietCreate, db: Session = Depends(get_db)):
    return create_diet(db, diet)

@router.put("/{diet_id}", response_model=DietResponse)
def update_existing_diet(diet_id: int, diet: DietUpdate, db: Session = Depends(get_db)):
    db_diet = update_diet(db, diet_id, diet)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    return db_diet

@router.delete("/{diet_id}", response_model=DietResponse)
def delete_existing_diet(diet_id: int, db: Session = Depends(get_db)):
    db_diet = delete_diet(db, diet_id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet not found")
    return db_diet