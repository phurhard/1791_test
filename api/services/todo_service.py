from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api.models.model import Todo
from api.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

def create_todo(db: Session, todo: TodoCreate, user_id: str) -> Todo:
    db_todo = Todo(content=todo.content, user_id=user_id, title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: str) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    return db.query(Todo).offset(skip).limit(limit).all()

def update_todo(db: Session, todo_id: str, todo: TodoUpdate, user_id: str) -> Optional[Todo]:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo and str(db_todo.user_id) == user_id:
        if db_todo:
            for var, value in todo.model_dump(exclude_unset=True).items():
                setattr(db_todo, var, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: str, user_id: str) -> bool:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo and str(db_todo.user_id) == user_id:
        db.delete(db_todo)
        db.commit()
        return True
    return False
