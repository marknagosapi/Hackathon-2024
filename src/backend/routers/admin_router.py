from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.admin_schema import Admin,AdminSchema 
from schemas.token_schema import Token
from services.admin_service import AdminService
from loguru import logger

logger.add("admin_router.log",  level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss.SSS} - {level: <8} - {message}")

router = APIRouter()

admin_service= AdminService()


@router.get("/admin/me/", response_model=Admin)
async def read_admins_me(
    current_admin: Annotated[Admin, Depends(admin_service.get_current_admin)]
):
    logger.info(f"Endpoint '/admin/me/' called")

    return current_admin


@router.get("/admins/", status_code=status.HTTP_200_OK)
def get_admins():
    logger.info(f"Endpoint '/admins/' called")
    
    admins= admin_service.get_admins()
    
    return admins


@router.post('/admins/add', status_code=status.HTTP_201_CREATED)
def add_admins(admin: AdminSchema):
    logger.info(f"Endpoint '/admins/add/' called")

    return admin_service.register_admin(admin)


@router.delete('/admins/delete/', status_code=status.HTTP_200_OK)
def delete_admins_by_email(current_admin: Annotated[Admin, Depends(admin_service.get_current_admin)]):
    logger.info(f"Endpoint '/admins/delete/' called")

    admin_service.delete_user(current_admin)

    return {"message":"Account deleted"}
