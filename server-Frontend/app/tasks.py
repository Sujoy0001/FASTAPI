from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import Task


@celery_app.task
def notify_task_created(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            # Placeholder for notification logic (email, webhook, etc.)
            print(f"[Celery] Task created: {task.title} (id={task.id})")
            return True
        return False
    finally:
        db.close()
