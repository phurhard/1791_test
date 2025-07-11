from fastapi import Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from api.database.database import init_db
from api.models.model import User
from api.core.settings import settings
import bcrypt

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: int = 10) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Function to decode a JWT token
def decode_token(token: str) -> str:
    try:
        payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(init_db)) -> User:
    try:
        user_id = decode_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except ValueError as e:
        # Handle token-related issues (e.g., expired or invalid token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.args[0]),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        # Handle token-related issues (e.g., expired or invalid token)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )

def get_pass_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass_hash(password: str, hashed_password: str) -> bool:
    """Check a password against a hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
