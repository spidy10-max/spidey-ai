"""Spidey AI - Main Entry Point"""

from fastapi import FastAPI
from src.api.routes import router
from src.core.config import settings
from src.utils.logger import spidey_logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    spidey_logger.info(f"Spidey AI v{settings.APP_VERSION} starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    spidey_logger.info("Spidey AI shutting down...")
