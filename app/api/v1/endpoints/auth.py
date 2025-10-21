from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserResponse
from app.db.crud import create_user, get_user_by_username
from app.db.database import get_db
from app.utils.security import create_jwt_token, verify_password
router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db, user)

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"user_id": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
