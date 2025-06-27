from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import timedelta
from api.models.model import User
from api.schemas.user import UserCreate, UserUpdate, UserLogin, TokenResponse, UserResponse
from api.utils.dependencies import get_pass_hash, check_pass_hash, create_access_token, decode_token

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

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticates a user by checking their username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The plain-text password provided by the user.

    Returns:
        Optional[User]: The user object if authentication is successful, otherwise None.
    """
    user = get_user_by_username(db, username)
    if not user or not check_pass_hash(password, str(user.password)):
        return None
    return user

def login_user(db: Session, user_login: UserLogin) -> TokenResponse:
    """
    Logs in a user, authenticates them, and generates access and refresh tokens.

    Args:
        db (Session): The database session.
        user_login (UserLogin): The user login credentials.

    Returns:
        TokenResponse: An object containing user details, access token, and refresh token.

    Raises:
        HTTPException: If authentication fails.
    """
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=int(access_token_expires.total_seconds() / 60)
    )
    refresh_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=int(refresh_token_expires.total_seconds() / 60)
    )

    return TokenResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
    """
    Validates the refresh token and issues a new access token (and refresh token).

    Args:
        db (Session): The database session.
        refresh_token (str): The refresh token.

    Returns:
        TokenResponse: An object containing user details, new access token, and refresh token.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    """
    try:
        user_id = decode_token(refresh_token)
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=7)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=int(access_token_expires.total_seconds() / 60)
        )
        new_refresh_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=int(refresh_token_expires.total_seconds() / 60)
        )
        return TokenResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
