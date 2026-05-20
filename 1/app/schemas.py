from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=80)
    description: Optional[str] = None
    status: TaskStatus
    priority: int = Field(..., ge=1, le=5)

    @field_validator("title")
    def validate_title(cls, v):
        if len(v) < 3:
            raise ValueError("title must be at least 3 characters")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: int
    owner_id: int

class TaskUpdateStatus(BaseModel):
    status: TaskStatus