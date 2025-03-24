from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.core.security import hash_password, verify_password, create_jwt_token
from app.core.database import users_collection
from datetime import timedelta
from app.core.auth import authenticate_user

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    try: 
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
        user.password = hash_password(user.password)
        await users_collection.insert_one(user.dict())
        return {"message": f"User {user.name} registered successfully"}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await authenticate_user(form_data)