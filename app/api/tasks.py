from fastapi import APIRouter, HTTPException, Depends
from app.models.task import Task
from app.core.database import tasks_collection
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def add_task(task: Task):
    try: 
        await tasks_collection.insert_one(task.dict())
        return {"message": "Task added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_all_tasks():
    try: 
        cursor = tasks_collection.find({}, {'_id': 0})  # Exclude _id field from results
        tasks = await cursor.to_list(length=None)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}")
async def update_task(task_id: str, task: Task):
    try: 
        result = await tasks_collection.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": task.dict(exclude={'id'})}
        )
    
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try: 
        result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}")
async def get_task_by_id(task_id: str):
    try: 
        task = await tasks_collection.find_one({"_id": ObjectId(task_id)}, {"_id": 0})
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))