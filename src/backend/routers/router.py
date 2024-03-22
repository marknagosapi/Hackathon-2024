from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.admin_schema import Admin,AdminSchema 
from schemas.token_schema import Token
from services.admin_service import AdminService
from services.user_service import UserService
from loguru import logger


router = APIRouter(
    prefix="", tags=["default"]
)

admin_service= AdminService()
user_service = UserService()

@router.get("/")
async def read_root():
    return {"message": "Hello, World"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):  
    logger.info(f"Endpoint '/token' called")

    user_info = user_service.get_user(form_data.username)
    admin_info = admin_service.get_admin(form_data.username)

    if user_info:
        return user_service.login_for_access_token(form_data.username, form_data.password)
    elif admin_info:
        return admin_service.login_for_access_token(form_data.username, form_data.password)
    else:
        raise HTTPException(status_code=400, detail="Invalid email address")