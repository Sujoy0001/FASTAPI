from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    status: str
    celery_task_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskStatusResponse(BaseModel):
    task_id: int
    status: str
    celery_task_id: Optional[str]
    celery_result: Optional[dict]
    completed: bool
    created_at: datetime
    updated_at: datetime