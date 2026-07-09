from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskStatusResponse
from app.tasks import notify_task_created
from app.celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(task: TaskCreate):
    db = SessionLocal()

    new_task = Task(
        title=task.title,
        description=task.description,
        importance=task.importance,
        status="pending"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Enqueue a background notification job
    try:
        celery_task = notify_task_created.delay(new_task.id)
        new_task.celery_task_id = celery_task.id
        new_task.status = "running"
        db.commit()
        db.refresh(new_task)
    except Exception as e:
        # If Celery is not running or broker unavailable, proceed without failing the request
        print(f"Celery task enqueue failed: {e}")

    db.close()
    return {"message": "Task created", "task": new_task}


@router.get("/")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return tasks


@router.get("/{task_id}")
def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}")
def update_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()
    db.close()

    return {"message": "Task completed"}
    

@router.delete("/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    db.close()

    return {"message": "Task deleted"}


@router.get("/{task_id}/status")
def get_task_status(task_id: int):
    """Get detailed task status including Celery task result"""
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get Celery task result if available
    celery_result = None
    celery_status = task.status
    
    if task.celery_task_id:
        try:
            celery_async_result = celery_app.AsyncResult(task.celery_task_id)
            celery_status = celery_async_result.status
            celery_result = {
                "status": celery_async_result.status,
                "ready": celery_async_result.ready(),
                "successful": celery_async_result.successful() if celery_async_result.ready() else None,
                "result": celery_async_result.result if celery_async_result.ready() else None,
            }
            
            # Update task status based on Celery result
            if celery_async_result.ready():
                if celery_async_result.successful():
                    task.status = "completed"
                else:
                    task.status = "failed"
        except Exception as e:
            print(f"Error checking Celery task status: {e}")

    return TaskStatusResponse(
        task_id=task.id,
        status=celery_status,
        importance=task.importance,
        celery_task_id=task.celery_task_id,
        celery_result=celery_result,
        completed=task.completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )