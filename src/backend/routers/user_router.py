from typing import Annotated
from fastapi import APIRouter, Depends, status
from schemas.user_schema import User, UserSchema
from services.user_service import UserService
from schemas.bill_schema import BillSchema
from loguru import logger


logger.add("user_router.log",  level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss.SSS} - {level: <8} - {message}")

router = APIRouter()

user_service= UserService()


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(user_service.get_current_user)]
):
    logger.info(f"Endpoint '/users/me/' called")

    return current_user


@router.get("/users/id/")
async def read_users_me(
    current_user: Annotated[User, Depends(user_service.get_current_user)]
):
    logger.info(f"Endpoint '/users/id/' called")

    user_id = user_service.get_user_id(current_user.email)
    return {"id":user_id} 


@router.get("/users/", status_code=status.HTTP_200_OK)
def get_users():
    logger.info(f"Endpoint '/users/' called")
    
    users= user_service.get_users()
    
    return users


@router.post('/users/add', status_code=status.HTTP_201_CREATED)
def add_user(user: UserSchema):
    logger.info(f"Endpoint '/users/add/' called")

    return user_service.register_user(user)


@router.delete('/users/delete/', status_code=status.HTTP_200_OK)
def delete_user_by_email(current_user: Annotated[User, Depends(user_service.get_current_user)]):
    logger.info(f"Endpoint '/users/delete/' called")

    user_service.delete_user(current_user)

    return {"message":"Account deleted"}

@router.post('/users/add_bill', status_code=status.HTTP_201_CREATED)
def add_bill(bill: BillSchema):
    logger.info(f"Endpoint '/users/add_bill/' called")

    return {bill.user_id}
