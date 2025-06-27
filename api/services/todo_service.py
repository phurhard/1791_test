import json
from typing import Optional, List
from openai import OpenAI
from sqlalchemy.orm import Session
from api.core.settings import settings
from api.models.model import Todo
from api.schemas.todo import TodoCreate, TodoUpdate
from datetime import datetime

client = OpenAI(api_key = settings.OPENAI_API_KEY)

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
    db_todo = Todo(content=todo.content, user_id=user_id, title=todo.title, priority=todo.priority, due_date=todo.due_date)
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


def analyze_productivity(db: Session) -> dict:
    """
    Analyze task completion data to generate productivity reports.

    Args:
        db (Session): The database session.

    Returns:
        dict: A dictionary containing productivity metrics and insights.
    """
    completed_tasks = db.query(Todo).filter(
        Todo.completed == True
    ).count()
    total_tasks = db.query(Todo).count()
    overdue_tasks = db.query(Todo).filter(
        Todo.due_date < datetime.now(),
        Todo.completed == False
    ).count()

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    insights = []

    if completion_rate < 50:
        insights.append("Consider prioritizing your tasks to improve completion rates.")
    if overdue_tasks > 0:
        insights.append(f"You have {overdue_tasks} overdue tasks. Try to complete them as soon as possible.")

    return {
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "overdue_tasks": overdue_tasks,
        "completion_rate": completion_rate,
        "insights": insights,
        "suggestions": generate_ai_suggestions({
            "completion_rate": completion_rate,
            "overdue_tasks": overdue_tasks,
            "completed_tasks": completed_tasks,
        }),
    }


def generate_ai_suggestions(data: dict) -> dict:
    """Returns AI suggestions based on user todo behavior"""
    
    # Build system prompt
    system_prompt = (
        "You are an advanced productivity assistant. Analyze the user's to-do list data and provide 3-5 personalized suggestions "
        "to help improve their productivity. Consider their completed tasks, overdue tasks, and task completion frequency. "
        "Return your response as a JSON object in the following format: "
        "{\"suggestions\": [\"suggestion 1\", \"suggestion 2\", \"suggestion 3\"]}. Do not include any text outside the JSON object."
    )

    # Construct a formatted message
    user_prompt = (
        f"Here is the user's task data:\n\n"
        f"Completed Tasks: {data.get('completed_tasks', [])}\n"
        f"Overdue Tasks: {data.get('overdue_tasks', [])}\n"
        f"Pending Tasks: {data.get('pending_tasks', [])}\n\n"
    )

    if "completion_history" in data:
        user_prompt += "Completion History:\n"
        for entry in data["completion_history"]:
            user_prompt += f"- {entry['date']}: {entry['completed_count']} tasks completed\n"

    user_prompt += "\nPlease provide tailored suggestions."

    # Chat completion call
    response = client.responses.create(
        model="gpt-4o",
        instructions=system_prompt,
        input=user_prompt,
        temperature=0.7
    )

    output = response.output_text.strip()
    try:
        # Try to parse the output as JSON
        result = json.loads(output)
        if isinstance(result, dict) and "suggestions" in result:
            return result
        # If not in expected format, fallback
        return {"suggestions": result if isinstance(result, list) else [str(result)]}
    except Exception:
        # Fallback: return the raw output as a single suggestion
        return {"suggestions": [output]}
