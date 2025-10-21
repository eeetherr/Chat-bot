import aioredis
from app.config import settings
import logging

logger = logging.getLogger(__name__)
redis = aioredis.from_url(settings.REDIS_URL)

async def get_cached_response(query: str):
    try:
        return await redis.get(query)
    except Exception as e:
        logger.error(f"Redis error: {e}")
        return None

async def set_cached_response(query: str, response: str):
    try:
        await redis.set(query, response, ex=3600)  # Cache for 1 hour
    except Exception as e:
        logger.error(f"Redis error: {e}")
