from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date


class TaskStatus(str, Enum):
    pending = "в ожидании"
    in_progress = "в работе"
    completed = "завершено"


class TaskPriority(str, Enum):
    low = "низкий"
    medium = "средний"
    high = "высокий"


class Task(BaseModel):
    id: int
    task_id: Optional[int]
    title: str
    description: str
    status: TaskStatus
    priority: Optional[TaskPriority] = None
    created_at: Optional[date] = None
