from fastapi import FastAPI, APIRouter
from src.api import app as all

api_router = APIRouter()
api_router.include_router(all)
app = FastAPI()
app.include_router(api_router)