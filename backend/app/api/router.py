from app.api.endpoints import health
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
