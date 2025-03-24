from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Optional, Dict
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.database import users_collection
from passlib.context import CryptContext
from bson.objectid import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="1")
            
        # Get full user data from database
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise HTTPException(status_code=401, detail="2")
            
        return {
            "user_id": user_id,
            "email": user["email"],
            "name": user["name"]
        }
        
    except JWTError:
        raise HTTPException(status_code=401, detail="3")

async def authenticate_user(form_data: OAuth2PasswordRequestForm) -> Dict:
    user = await users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = jwt.encode(
        {"user_id": str(user["_id"])},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
