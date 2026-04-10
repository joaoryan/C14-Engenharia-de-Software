from fastapi import APIRouter

from app.api.endpoints.user import router as user_router
from app.api.endpoints.diet import router as diet_router
from app.api.endpoints.user_diet import router as user_diet_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(diet_router, prefix="/diets", tags=["diets"])
api_router.include_router(user_diet_router, prefix="/users", tags=["user-diets"])