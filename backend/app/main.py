import time
from pathlib import Path

import uvicorn
from app.api.router import api_router
from app.core.config import settings
from app.core.logging_config import get_logger
from app.db import pins as pins_service
from app.db.mongodb import mongodb
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

logger = get_logger("main")

app = FastAPI(
    title="FastAPI Backend",
    description="A FastAPI backend with MongoDB",
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log request and response information."""
    start_time = time.time()

    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client=request.client.host if request.client else None,
    )

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=f"{process_time:.4f}s",
    )

    return response


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint that provides basic API information.

    Returns:
        HTMLResponse: HTML page with API information
    """
    logger.info("Root endpoint accessed")

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT,
        },
    )


@app.on_event("startup")
async def startup_event():
    """Execute actions on application startup."""
    logger.info(
        "Starting application",
        version=settings.API_VERSION,
        environment=settings.ENVIRONMENT,
    )
    await mongodb.connect()
    await pins_service.create_indexes()


@app.on_event("shutdown")
async def shutdown_event():
    """Execute actions on application shutdown."""
    logger.info("Shutting down application")
    await mongodb.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
    )
