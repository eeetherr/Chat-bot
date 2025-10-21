from threading import Thread
from sqlalchemy.orm import Session
from app.api.schemas.message import MessageCreate
from app.api.schemas.thread import ThreadCreate
from app.api.schemas.user import UserCreate
from app.models.message import Message
from app.models.user import User
from app.utils.security import hash_password

# User
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

# Thread
def create_thread(db: Session, thread: ThreadCreate, user_id: str):
    new_thread = Thread(title=thread.title, thread_id=thread.thread_id, user_id=user_id)
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

def get_thread_by_id(db: Session, thread_id: str, user_id: str):
    return db.query(Thread).filter(Thread.thread_id == thread_id, Thread.user_id == user_id).first()

def delete_thread(db: Session, thread_id: str, user_id: str):
    thread = db.query(Thread).filter(Thread.thread_id == thread_id, Thread.user_id == user_id).first()
    if thread:
        db.delete(thread)
        db.commit()
        return True
    return False

def get_thread_with_messages(db: Session, thread_id: str, user_id: str):
    return db.query(Thread).filter(Thread.thread_id == thread_id, Thread.user_id == user_id).first()


# Message
def create_message(db: Session, message: MessageCreate):
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_messages_by_thread(db: Session, thread_id: str):
    return db.query(Message).filter(Message.thread_id == thread_id).order_by(Message.created_at).all()

