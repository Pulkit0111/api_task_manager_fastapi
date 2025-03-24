from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.tasks import router as task_router

app = FastAPI(
    title="Task Manager API",
    description="A REST API for managing tasks and users",
    version="1.0.0"
)

app.include_router(
    users_router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    task_router,
    prefix="/api/tasks",
    tags=["Tasks"]
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "This is a task manager API"}