from pydantic import BaseModel
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int