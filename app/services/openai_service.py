from openai import OpenAI
from app.config import settings
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def get_response(query: str) -> AsyncGenerator[str, None]:
    """
    Get a streamed response from OpenAI's API for a given query.

    :param query: The user query to send to OpenAI's API.
    :yield: Chunks of the response content as they are received.
    """
    try:
        # Create a stream of completions
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a very good chatbot."},
                {"role": "user", "content": query}
            ],
            stream=True,
        )

        # Process the stream and yield chunks of content
        for chunk in stream:
            delta_content = chunk.choices[0].delta.content  # Directly access content attribute
            if delta_content:  # Check if content is not None
                yield delta_content

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        yield f"Error: {str(e)}"
