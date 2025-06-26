from fastapi import APIRouter, Depends, HTTPException
from api.models.model import User
from api.utils.dependencies import get_current_user
from sqlalchemy.orm import Session
from api.database.database import init_db
from api.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from api.services.todo_service import create_todo, get_todo, get_todos, update_todo, delete_todo

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    return create_todo(db, todo, str(current_user.id))

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo_endpoint(todo_id: str, db: Session = Depends(init_db)):
    todo = get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/", response_model=list[TodoResponse])
def read_todos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(init_db)):
    todos = get_todos(db, skip=skip, limit=limit)
    return todos

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: str, todo: TodoUpdate, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    updated_todo = update_todo(db, todo_id, todo, str(current_user.id))
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str, db: Session = Depends(init_db), current_user: User = Depends(get_current_user)):
    deleted_todo = delete_todo(db, todo_id, str(current_user.id))
    if not deleted_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted_todo
