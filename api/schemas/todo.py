from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=5)
    completed: bool = False
    priority: Optional[int] = Field(None, ge=1, le=3)  # 1: high, 2: medium, 3: low
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[int] = Field(None, ge=1, le=3)  # 1: high, 2: medium, 3: low
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    content: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
