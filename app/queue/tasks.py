from app.queue.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def log_interaction(user_id: int, query: str, response: str):
    try:
        # Log user interactions or save to database
        logger.info(f"Logged interaction: {user_id}, {query}, {response}")
    except Exception as e:
        logger.error(f"Logging error: {e}")
