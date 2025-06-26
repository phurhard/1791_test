from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database.database import init_db
from api.schemas.user import UserCreate, UserUpdate, UserResponse
from api.services.user_service import create_user, get_user, get_users, update_user, delete_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(init_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        UserResponse: The created user.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    try:
        return create_user(db, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        )

@router.get("/{user_id}", response_model=UserResponse)
def read_user_endpoint(user_id: str, db: Session = Depends(init_db)):
    """
    Retrieve a single user by ID.

    Args:
        user_id (str): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The retrieved user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
def read_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(init_db)):
    """
    Retrieve a list of users.

    Args:
        skip (int): The number of users to skip.
        limit (int): The maximum number of users to return.
        db (Session): The database session.

    Returns:
        list[UserResponse]: A list of users.
    """
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: str, user: UserUpdate, db: Session = Depends(init_db)):
    """
    Update an existing user.

    Args:
        user_id (str): The ID of the user to update.
        user (UserUpdate): The updated user data.
        db (Session): The database session.

    Returns:
        UserResponse: The updated user.

    Raises:
        HTTPException: If the user is not found or an error occurs during update.
    """
    try:
        updated_user = update_user(db, user_id, user)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except HTTPException as e:
        raise e

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(init_db)):
    """
    Delete a user by ID.

    Args:
        user_id (str): The ID of the user to delete.
        db (Session): The database session.

    Returns:
        UserResponse: The deleted user.

    Raises:
        HTTPException: If the user is not found.
    """
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
