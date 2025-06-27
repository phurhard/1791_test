from fastapi import APIRouter, Depends, HTTPException
from api.models.model import User
from api.utils.dependencies import get_current_user
from sqlalchemy.orm import Session
from api.database.database import init_db
from api.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from api.services.todo_service import create_todo, get_todo, get_todos, update_todo, delete_todo
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")
router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    """
    Create a new todo item.

    Args:
        todo (TodoCreate): The todo data to create.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TodoResponse: The created todo item.
    """
    return create_todo(db, todo, str(current_user.id))

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo_endpoint(todo_id: str, db: Session = Depends(init_db)):
    """
    Retrieve a single todo item by ID.

    Args:
        todo_id (str): The ID of the todo item to retrieve.
        db (Session): The database session.

    Returns:
        TodoResponse: The retrieved todo item.

    Raises:
        HTTPException: If the todo item is not found.
    """
    todo = get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/", response_model=list[TodoResponse])
def read_todos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(init_db)):
    """
    Retrieve a list of todo items.

    Args:
        skip (int): The number of todo items to skip.
        limit (int): The maximum number of todo items to return.
        db (Session): The database session.

    Returns:
        list[TodoResponse]: A list of todo items.
    """
    todos = get_todos(db, skip=skip, limit=limit)
    return todos

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: str, todo: TodoUpdate, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    """
    Update an existing todo item.

    Args:
        todo_id (str): The ID of the todo item to update.
        todo (TodoUpdate): The updated todo data.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TodoResponse: The updated todo item.

    Raises:
        HTTPException: If the todo item is not found.
    """
    updated_todo = update_todo(db, todo_id, todo, str(current_user.id))
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    """
    Delete a todo item by ID.

    Args:
        todo_id (str): The ID of the todo item to delete.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        bool: True if the todo item was deleted, False otherwise.

    Raises:
        HTTPException: If the todo item is not found.
    """
    deleted_todo = delete_todo(db, todo_id, str(current_user.id))
    if not deleted_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted_todo

@router.post("/nlp/", response_model=TodoResponse)
def create_todo_nlp_endpoint(description: str, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    """
    Create a new todo item from natural language input.

    Args:
        description (str): The natural language description of the todo item.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        TodoResponse: The created todo item.
    """
    # Process the natural language input
    doc = nlp(description)
    task_description = " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])
    print(f'doc: {doc}')
    print(f"description: {description}")
    
    # Enhance parsing to capture task details
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    due_date = None
    for entity in entities:
        if entity[1] == "DATE":
            due_date = entity[0]
            print(f"due date: {due_date}")
    
    # Create a TodoCreate object with the task description and due date
    todo_data = TodoCreate(title=task_description, content="No additional details provided")  # Placeholder content
    
    return create_todo(db, todo_data, str(current_user.id))
