from fastapi import APIRouter
from .endpoints import chatbot, health

api_router = APIRouter()
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
