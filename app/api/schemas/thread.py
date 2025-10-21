from pydantic import BaseModel
import uuid
from datetime import datetime

class ThreadBase(BaseModel):
    title: str
    thread_id: str

class ThreadCreate(ThreadBase):
    pass

class ThreadResponse(ThreadBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
