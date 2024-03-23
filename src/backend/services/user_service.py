from datetime import  datetime, timedelta
import os
import time
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from schemas.token_schema import TokenData, TokenCreationalData
from repositories.user_repository import UserRepository
from repositories.bill_repository import BillRepository
from repositories.item_repository import ItemRepository
from repositories.level_repository import LevelRepository
from repositories.admin_repository import AdminRepository
from schemas.user_schema import  UserSchema
from schemas.bill_schema import BillSchema,BillInDb
from schemas.item_schema import ItemSchema
from models.user import User
from helper.user_utilities import get_password_hash,verify_password
from helper.dependencies import oauth2_scheme, db
from loguru import logger
from datetime import datetime


TAG = "UserService"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class UserService:
    def __init__(self):
        self.db = db
        self.user_repository = UserRepository(db)
        self.bill_repository = BillRepository(db)
        self.item_repository = ItemRepository(db)
        self.level_repository = LevelRepository(db)
        self.adminRepository = AdminRepository(db)



    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.get_user(email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user


    def get_user(self, email: str):
        logger.info(f"{TAG} = get_user() -  called")

        user = self.user_repository.get_user(email)

        if not user:
            return False
        return user


    def get_user_id(self, email: str):
        logger.info(f"{TAG} = get_user_id() -  called")

        user_id = self.user_repository.get_user_id(email)

        if not user_id:
            return False
        

        return user_id


    def get_user_bills(self, user: User):
        logger.info(f"{TAG} = get_user_bills() - called")
        
        db_bills = self.bill_repository.find_bills(user.id)
        user_bills = []

        for db_bill in db_bills:
            market_name = self.adminRepository.get_market_name(db_bill.admin_id)

            bill_dict = {
                "user_id": db_bill.user_id,
                "admin_id": db_bill.admin_id,
                "market_name": market_name,
                "date": db_bill.date,
                "item_number": db_bill.item_number,
                "total": db_bill.total,
            }

            user_bills.append(bill_dict)

        return user_bills

    def create_bill_dict(self, db_bill):
        
        if not db_bill:  
            return None

        db_items = self.item_repository.find_items_by_bill_id(db_bill.id)
        market_name = self.adminRepository.get_market_name(db_bill.admin_id)

        bill_dict = {
            "user_id": db_bill.user_id,
            "admin_id": db_bill.admin_id,
            "market_name": market_name,
            "date": db_bill.date,
            "item_number": db_bill.item_number,
            "total": db_bill.total,
            "items": [ItemSchema(name=item.name, quantity=item.quantity, unique_price=item.unique_price, total_price=item.total_price) for item in db_items]
        }

        return bill_dict 



    def get_user_bill_by_id(self,user:User, bill_id:int):
        logger.info(f"{TAG} = get_user_bills() -  called")

        db_bill = self.bill_repository.find_bill_by_id(bill_id)

        bill_dict = self.create_bill_dict(db_bill)

        return bill_dict


    def get_current_bill(self, user:User):
        logger.info(f"{TAG} = get_current_bill() -  called")

        db_bill = self.bill_repository.find_current_bill(user.id)

        if db_bill is None:
            return None
        bill_dict = self.create_bill_dict(db_bill)

        user_points = self.user_repository.add_points_for_user(int(db_bill.total), user)
        level_id = self.level_repository.get_level_by_points(user_points)
        self.user_repository.update_level(level_id[0], user)

        return bill_dict



    def get_users(self):
        logger.info(f"{TAG} = get_users() -  called")
        users = self.user_repository.get_users()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="No users found")
        return users
    

    def delete_user(self, user):
        logger.info(f"{TAG} = delete_user() -  called")
        
        self.user_repository.delete_user(user)


    def create_access_token(self, data: TokenCreationalData):
        logger.info(f"{TAG} = create_access_token - called ")

        to_encode = data.model_dump()

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def create_access_token_for_user(self, email: str) -> str:
        logger.info(f"{TAG} = create_access_token_for_user - called ")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if access_token_expires:
            expire = datetime.utcnow() + access_token_expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        token_creatinal_data=TokenCreationalData(sub=email,exp=expire)
        access_token = self.create_access_token(token_creatinal_data)
        return access_token

    

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        logger.info(f"{TAG} = get_current_user - called ")
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        
        except JWTError:
            raise credentials_exception
        
        user = self.get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        
        return user


    def login_for_access_token(self, username: str, password: str):
        logger.info(f"{TAG} = login_for_access_token - called()")
        
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token_for_user(user.email)
        logger.info(f"User logged in with email: {user.email} token: {access_token}")
        
        return {"access_token": access_token, "token_type": "bearer", "user_type":type(user).__name__ }


    def register_user(self, user: UserSchema):
        logger.info(f"{TAG} = register_user() - called")

        db_user = self.user_repository.get_user(user.email)

        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered")

        hashed_password = get_password_hash(user.password)

        new_user = User(

            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
        )

        self.user_repository.add_user(new_user)

        return {"message": "Registration successful. User created."}
