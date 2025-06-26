from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.database import init_db
from api.models.model import User
from api.schemas.user import UserCreate, UserResponse
from api.services.user_service import create_user, get_user, get_users, update_user, delete_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(init_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user_endpoint(user_id: str, db: Session = Depends(init_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
def read_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(init_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(init_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(init_db)):
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
