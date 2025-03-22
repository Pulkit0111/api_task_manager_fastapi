from fastapi import FastAPI
from app.api.users import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "This is a task manager API"}