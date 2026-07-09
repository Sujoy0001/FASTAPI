from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    importance = Column(String, default="normal")
    completed = Column(Boolean, default=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    celery_task_id = Column(String, nullable=True)  # Store Celery task ID for result tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)