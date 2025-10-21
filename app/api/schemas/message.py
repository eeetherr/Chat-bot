from pydantic import BaseModel
import uuid
from datetime import datetime

class MessageBase(BaseModel):
    thread_id: uuid.UUID
    sender: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
