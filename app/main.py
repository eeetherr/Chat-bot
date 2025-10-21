from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.v1.routers import api_router
from .config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield  # Application runs during this yield
    logger.info("Shutting down...")

# Create FastAPI instance with lifespan
app = FastAPI(title="Chatbot API", version="1.0.0", lifespan=lifespan)

# Register routes
app.include_router(api_router, prefix=settings.API_V1_STR)
