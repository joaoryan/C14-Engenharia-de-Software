from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.diet import DietResponse
from app.services.user_diet import (
    assign_diet_to_user,
    get_user_diets,
    unassign_diet_from_user,
)

router = APIRouter()


@router.get("/{user_id}/diets", response_model=list[DietResponse])
def read_user_diets(user_id: int, db: Session = Depends(get_db)):
    diets = get_user_diets(db, user_id)
    if diets is None:
        raise HTTPException(status_code=404, detail="User not found")
    return diets


@router.put("/{user_id}/diets/{diet_id}", response_model=DietResponse)
def assign_diet(user_id: int, diet_id: int, db: Session = Depends(get_db)):
    diet, error = assign_diet_to_user(db, user_id, diet_id)

    if error == "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")
    if error == "diet_not_found":
        raise HTTPException(status_code=404, detail="Diet not found")

    return diet


@router.delete("/{user_id}/diets/{diet_id}", response_model=DietResponse)
def unassign_diet(user_id: int, diet_id: int, db: Session = Depends(get_db)):
    diet, error = unassign_diet_from_user(db, user_id, diet_id)

    if error == "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")
    if error == "diet_not_found":
        raise HTTPException(status_code=404, detail="Diet not found")
    if error == "diet_not_assigned_to_user":
        raise HTTPException(
            status_code=400,
            detail="Diet is not assigned to this user"
        )

    return diet