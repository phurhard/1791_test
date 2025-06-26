from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.models.model import User
from api.schemas.user import UserCreate, UserUpdate
from api.utils.dependencies import get_pass_hash

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    return db.query(User).filter(
        or_(User.email == email)).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    return db.query(User).filter(
        or_(User.username == username)).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the email or username is already registered.
    """
    existing_email = get_user_by_email(db, user.email)
    existing_username = get_user_by_username(db, user.username)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
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
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to retrieve.

    Returns:
        List[User]: A list of user objects.
    """
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user: UserUpdate) -> Optional[User]:
    """
    Update an existing user in the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to update.
        user (UserUpdate): The updated user data.

    Returns:
        Optional[User]: The updated user object if found, otherwise None.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for var, value in vars(user).items():
            setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> bool:
    """
    Delete a user from the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user to delete.

    Returns:
        bool: True if the user was deleted, False otherwise.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
