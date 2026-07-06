from app.database import SessionLocal, engine, Base
from app.models import Task
from app.tasks import notify_task_created

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    task = db.query(Task).first()
    if not task:
        task = Task(title="Test Task", description="Created for test")
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"Created Task id={task.id}")
    else:
        print(f"Using existing Task id={task.id}")

    # Run the Celery task synchronously in-process
    result = notify_task_created.run(task.id)
    print("notify_task_created.run returned:", result)
finally:
    db.close()
