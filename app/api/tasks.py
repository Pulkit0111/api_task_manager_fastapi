from fastapi import APIRouter, HTTPException, Depends
from app.models.task import Task
from app.core.database import tasks_collection
from bson import ObjectId
from app.core.auth import get_current_user


router = APIRouter()

@router.post("/")
async def add_task(task: Task, current_user: dict = Depends(get_current_user)):
    try:
        task_data = task.dict(exclude_unset=True)  # Only include set fields
        task_data["created_by"] = current_user["user_id"]  # Associate task with current user
        await tasks_collection.insert_one(task_data)
        return {"message": "Task added successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/")
async def get_all_tasks(current_user: dict = Depends(get_current_user)):
    try:
        cursor = tasks_collection.find(
            {"created_by": current_user["user_id"]},
            {"created_by": 0}
        )
        tasks = await cursor.to_list(length=None)
        
        for task in tasks:
            task["_id"] = str(task["_id"])
            
        return tasks
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.put("/{task_id}")
async def update_task(task_id: str, task: Task, current_user: dict = Depends(get_current_user)):
    try:
        existing_task = await tasks_collection.find_one({
            "_id": ObjectId(task_id),
            "created_by": current_user["user_id"]
        })
        
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        result = await tasks_collection.update_one(
            {
                "_id": ObjectId(task_id),
                "created_by": current_user["user_id"]
            },
            {"$set": task.dict(exclude_unset=True)}
        )
        
        return {"message": "Task updated successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # Check if task exists and belongs to current user
        existing_task = await tasks_collection.find_one({
            "_id": ObjectId(task_id),
            "created_by": current_user["user_id"]
        })
        
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        result = await tasks_collection.delete_one({
            "_id": ObjectId(task_id),
            "created_by": current_user["user_id"]
        })
        
        return {"message": "Task deleted successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.patch("/{task_id}")
async def toggle_task_status(task_id: str, current_user: dict = Depends(get_current_user)):
    try:
        task = await tasks_collection.find_one({
            "_id": ObjectId(task_id),
            "created_by": current_user["user_id"]
        })

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Toggle the status field
        new_status = not task["completed"]
        
        await tasks_collection.update_one(
            {
                "_id": ObjectId(task_id),
                "created_by": current_user["user_id"]
            },
            {"$set": {"completed": new_status}}
        )

        return {"message": f"Task status updated successfully to {'completed' if new_status else 'pending'}"}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

