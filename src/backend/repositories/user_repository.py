from models.user import User
from sqlalchemy.orm import Session
from loguru import logger

TAG = "UserRepository"

class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_user(self, email: str):
        logger.info(f"{TAG} = get_user() -  called")
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def get_user_id(self, email):
        logger.info(f"{TAG} = get_user_id() -  called")
        
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return user.id
        else:
            return None


    def get_users(self):
        logger.info(f"{TAG} = get_users() -  called")
        users = self.db.query(User).all()
        return users


    def add_user(self, user: User):
        logger.info(f"{TAG} = add_user() -  called")

        self.db.add(user)
        self.db.commit()

        return user


    def delete_user(self, user: User):
        logger.info(f"{TAG} = delete_user() -  called")
        
        self.db.delete(user)

        self.db.commit


    # def get_refresh_token(self, refresh_token:str):
    #     logger.info(f"{TAG} = get_refresh_token() -  called")
    #     token = self.db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    #     return token


    # def add_refresh_token(self, refresh_token: RefreshToken):
    #     logger.info(f"{TAG} = add_refresh_token() -  called")

    #     self.db.add(refresh_token)
    #     self.db.commit()

    #     return refresh_token
