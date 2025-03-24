from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.core.security import hash_password, verify_password, create_jwt_token
from app.core.database import users_collection
from datetime import timedelta

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    try: 
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
        user.password = hash_password(user.password)
        await users_collection.insert_one(user.dict())
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(email: str, password: str):
    try: 
        user = await users_collection.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
        token = create_jwt_token(
            {"sub": user["email"]},
            timedelta(hours=12)
        )
        return {"message": "Logged in successfully", "access_token": token, "token_type": "Bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))