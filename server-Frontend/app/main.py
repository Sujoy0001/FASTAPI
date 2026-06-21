from fastapi import FastAPI
from app.database import engine, Base
from app.routes.task import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.include_router(task_router)

@app.get("/api")
def home():
    return {"message": "API Running"}

app.frontend("/", directory="dist", fallback="index.html")