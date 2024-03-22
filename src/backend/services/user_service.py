from datetime import  datetime, timedelta
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from schemas.token_schema import TokenData, TokenCreationalData
from repositories.user_repository import UserRepository
from schemas.user_schema import  UserSchema
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
        
        return {"access_token": access_token, "token_type": "bearer"}


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
