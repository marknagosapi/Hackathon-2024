from datetime import  datetime, timedelta
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from schemas.token_schema import TokenData, TokenCreationalData
from repositories.admin_repository import AdminRepository
from repositories.bill_repository import BillRepository
from repositories.item_repository import ItemRepository
from schemas.admin_schema import  AdminSchema
from schemas.bill_schema import BillSchema, BillInDb
from schemas.item_schema import  ItemInDb
from models.admin import Admin
from helper.user_utilities import get_password_hash,verify_password
from helper.dependencies import oauth2_scheme, db
from helper.utilities import send_post_request, generate_random_items
from loguru import logger
from datetime import datetime


TAG = "AdminService"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class AdminService:
    def __init__(self):
        self.db = db
        self.admin_repository = AdminRepository(db)



    def qr_scanned(self, user_id: int, current_admin:Admin):
        logger.info(f"{TAG} = qr_scanned() -  called")

        self.bill_repository = BillRepository(db)
        self.item_repository = ItemRepository(db)


        admin_id = self.admin_repository.get_user_id(current_admin.email)

        bill = BillSchema(
            user_id=user_id,
            admin_id=admin_id
        )

        items = generate_random_items(12)
        bill.items = items

        item_number = len(items)

        total_price = sum(item["total_price"] for item in items)

        bill.item_number = item_number
        bill.total = total_price

        db_bill = self.bill_repository.create_bill(BillInDb(**bill.model_dump()))
        # [setattr(ItemInDb(**item), 'bill_id', db_bill.id) for item in items]

        # self.item_repository.create_items(items)
        for item in items:
            db_item = ItemInDb(**item)
            db_item.bill_id = db_bill.id
            self.item_repository.create_item(db_item)

        return db_bill


    def authenticate_admin(self, email: str, password: str):
        admin = self.admin_repository.get_admin(email)
        if not admin:
            return False
        if not verify_password(password, admin.password):
            return False
        return admin


    def get_admin(self, email: str):
        logger.info(f"{TAG} = get_admin() -  called")

        admin = self.admin_repository.get_admin(email)

        if not admin:
            return False
        return admin


    def get_admins(self):
        logger.info(f"{TAG} = get_admins() -  called")
        admins = self.admin_repository.get_admins()
        if not admins:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="No admins found")
        return admins
    

    def delete_admin(self, admin):
        logger.info(f"{TAG} = delete_admin() -  called")
        
        self.admin_repository.delete_admin(admin)


    def create_access_token(self, data: TokenCreationalData):
        logger.info(f"{TAG} = create_access_token - called ")

        to_encode = data.model_dump()

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def create_access_token_for_admin(self, email: str) -> str:
        logger.info(f"{TAG} = create_access_token_for_admin - called ")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if access_token_expires:
            expire = datetime.utcnow() + access_token_expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        token_creatinal_data=TokenCreationalData(sub=email,exp=expire)
        access_token = self.create_access_token(token_creatinal_data)
        return access_token

    

    async def get_current_admin(self, token: Annotated[str, Depends(oauth2_scheme)]):
        logger.info(f"{TAG} = get_current_admin - called ")
        
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
        
        admin = self.get_admin(email=token_data.email)
        if admin is None:
            raise credentials_exception
        
        return admin


    def login_for_access_token(self, username: str, password: str):
        logger.info(f"{TAG} = login_for_access_token - called()")
        
        admin = self.authenticate_admin(username, password)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token_for_admin(admin.email)
        logger.info(f"Admin logged in with email: {admin.email} token: {access_token}")
        
        return {"access_token": access_token, "token_type": "bearer"}


    def register_admin(self, admin: AdminSchema):
        logger.info(f"{TAG} = register_admin() - called")

        db_admin = self.admin_repository.get_admin(admin.email)

        if db_admin:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered")

        hashed_password = get_password_hash(admin.password)

        new_user = Admin(

            first_name=admin.first_name,
            last_name=admin.last_name,
            email=admin.email,
            market_name=admin.market_name,
            password=hashed_password,
        )

        self.admin_repository.add_admin(new_user)

        return {"message": "Registration successful. Admin created."}
