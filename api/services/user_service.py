from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.model import User
from api.schemas.user import UserCreate, UserUpdate
from api.utils.dependencies import get_pass_hash

def get_user_by_email(db: Session, email: str, username: str) -> Optional[User]:
    return db.query(User).filter(
        or_(User.email == email, User.username == username)).first()

def create_user(db: Session, user: UserCreate) -> User:
    existing_user = get_user_by_email(db, user.email, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email/Username already registered"
        )

    password = get_pass_hash(user.password)
    db_user = User(
        username=user.username,
        password=password,
        email=user.email,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
