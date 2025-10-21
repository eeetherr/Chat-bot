import logging

logger = logging.getLogger(__name__)

def preprocess_text(text: str) -> str:
    try:
        # Example: Lowercase the text and strip leading/trailing spaces
        return text.lower().strip()
    except Exception as e:
        logger.error(f"Preprocessing error: {e}")
        raise
