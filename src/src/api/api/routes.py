"""
Spidey AI - API Routes
Saare endpoints yahan defined hain
"""

from fastapi import APIRouter
from src.core.config import settings

# Router instance
router = APIRouter()


@router.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is waking up!",
        "status": "active",
        "version": settings.APP_VERSION
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


@router.get("/about")
def about():
    return {
        "name": settings.APP_NAME,
        "creator": settings.CREATOR,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "tech_stack": ["Python", "FastAPI", "OpenAI"]
    }