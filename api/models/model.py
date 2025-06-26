from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import func
from datetime import datetime, timezone
import uuid
from api.database.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class User(BaseModel):
    __tablename__ = 'users'
    name = Column(String, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    todos = relationship("Todo", back_populates="user")

class Todo(BaseModel):
    __tablename__ = 'todos'
    title = Column(String)
    content = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="todos")

