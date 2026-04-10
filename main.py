from fastapi import FastAPI
from app.api import api_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Diet"}

app.include_router(api_router, prefix="/api")

Base.metadata.create_all(bind=engine)