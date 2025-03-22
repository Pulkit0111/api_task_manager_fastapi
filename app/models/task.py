from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str
    assigned_to: str
    priority: int
    due_date: datetime
    completed: bool = False