from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class UserUpdate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: str
    username: str
    name: str
    email: EmailStr
    created_at: datetime
