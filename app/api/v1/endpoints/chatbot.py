import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.message import MessageCreate
from app.api.schemas.thread import ThreadCreate, ThreadResponse
from app.db.crud import create_message, create_thread, get_messages_by_thread, get_thread_with_messages
from app.queue.tasks import log_interaction
from app.services.cache_service import get_cached_response, set_cached_response
from app.services.openai_service import get_response
from fastapi.responses import StreamingResponse
from app.db.database import get_db
from uuid import uuid4

from app.utils.security import get_current_user

router = APIRouter()

@router.post("/new_chat", response_model=ThreadResponse)
def new_chat(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    thread = ThreadCreate(title=f"Chat {uuid4().hex[:8]}", thread_id=str(uuid4()))
    return create_thread(db, thread, user_id)

@router.get("/continue_chat/{thread_id}", response_model=ThreadResponse)
def continue_chat(thread_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    thread = get_thread_with_messages(db, thread_id, user_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.post("/chat/{thread_id}")
async def chat(
    thread_id: str,
    query: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the thread exists
    thread = get_thread_with_messages(db, thread_id, user_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Attempt to fetch cached history from Redis
    cached_history = await get_cached_response(thread_id)
    if cached_history:
        history_messages = json.loads(cached_history)
    else:
        # Retrieve history from DB and cache it
        history = get_messages_by_thread(db, thread_id)
        history_messages = [
            {"role": "user" if msg.sender == "user" else "assistant", "content": msg.content}
            for msg in history
        ]
        await set_cached_response(thread_id, json.dumps(history_messages))

    # Add the user's query to the history
    history_messages.append({"role": "user", "content": query})
    new_user_message = MessageCreate(thread_id=thread_id, sender="user", content=query)
    create_message(db, new_user_message)

    # Generate the chatbot's response
    response_generator = get_response(query, history_messages)

    async def stream_response():
        response_content = ""
        async for chunk in response_generator:
            response_content += chunk
            yield chunk

        # Save the bot's response and log the interaction
        new_bot_message = MessageCreate(thread_id=thread_id, sender="bot", content=response_content)
        create_message(db, new_bot_message)
        await set_cached_response(thread_id, json.dumps(history_messages + [{"role": "assistant", "content": response_content}]))
        log_interaction.delay(user_id, query, response_content)  # Use Celery for logging

    return StreamingResponse(stream_response(), media_type="text/plain")
