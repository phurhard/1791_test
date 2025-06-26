from typing import Optional, List
from sqlalchemy.orm import Session
from api.models.model import Todo
from api.schemas.todo import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate, user_id: str) -> Todo:
    """
    Create a new todo item in the database.

    Args:
        db (Session): The database session.
        todo (TodoCreate): The todo data to create.
        user_id (str): The ID of the user creating the todo.

    Returns:
        Todo: The created todo object.
    """
    db_todo = Todo(content=todo.content, user_id=user_id, title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: str) -> Optional[Todo]:
    """
    Retrieve a todo item by its ID.

    Args:
        db (Session): The database session.
        todo_id (str): The ID of the todo item.

    Returns:
        Optional[Todo]: The todo object if found, otherwise None.
    """
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    """
    Retrieve a list of todo items from the database.

    Args:
        db (Session): The database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to retrieve.

    Returns:
        List[Todo]: A list of todo objects.
    """
    return db.query(Todo).offset(skip).limit(limit).all()

def update_todo(db: Session, todo_id: str, todo: TodoUpdate, user_id: str) -> Optional[Todo]:
    """
    Update an existing todo item in the database.

    Args:
        db (Session): The database session.
        todo_id (str): The ID of the todo item to update.
        todo (TodoUpdate): The updated todo data.
        user_id (str): The ID of the user attempting to update the todo.

    Returns:
        Optional[Todo]: The updated todo object if found and authorized, otherwise None.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo and str(db_todo.user_id) == user_id:
        if db_todo:
            for var, value in todo.model_dump(exclude_unset=True).items():
                setattr(db_todo, var, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: str, user_id: str) -> bool:
    """
    Delete a todo item from the database.

    Args:
        db (Session): The database session.
        todo_id (str): The ID of the todo item to delete.
        user_id (str): The ID of the user attempting to delete the todo.

    Returns:
        bool: True if the todo item was deleted and authorized, False otherwise.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo and str(db_todo.user_id) == user_id:
        db.delete(db_todo)
        db.commit()
        return True
    return False
