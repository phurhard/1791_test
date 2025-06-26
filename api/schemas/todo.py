from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    content: str = None
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: Optional[bool] = False


class TodoResponse(BaseModel):
    id: str
    title: str
    content: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str
    model_config = ConfigDict(from_attributes=True)
