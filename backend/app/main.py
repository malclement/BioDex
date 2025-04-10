import logging
import time

import uvicorn
from app.api.router import api_router
from app.core.config import settings
from app.core.logging_config import get_logger
from app.db.mongodb import mongodb
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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


@app.get("/")
async def root():
    """
    Root endpoint that provides basic API information.

    Returns:
        dict: Basic information about the API
    """
    logger.info("Root endpoint accessed")

    return {
        "name": "FastAPI Backend",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "description": "A FastAPI backend with MongoDB",
        "docs_url": "/docs",
        "health_check": "/health",
    }


app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Execute actions on application startup."""
    logger.info(
        "Starting application",
        version=settings.API_VERSION,
        environment=settings.ENVIRONMENT,
    )
    await mongodb.connect()


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
