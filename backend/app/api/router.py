from app.api.endpoints import health
from app.api.endpoints import pins
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(pins.router, tags=["Pins"])
