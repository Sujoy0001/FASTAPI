from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "the server is running good!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

