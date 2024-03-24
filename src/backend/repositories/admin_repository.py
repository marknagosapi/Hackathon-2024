from models.admin import Admin
from models.item import Item
from models.bill import Bill
from sqlalchemy.orm import Session
from loguru import logger


TAG = "AdminRepository"

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_admin(self, email: str):
        logger.info(f"{TAG} = get_admin() -  called")
        admin = self.db.query(Admin).filter(Admin.email == email).first()
        return admin

    def get_user_id(self, email):
        logger.info(f"{TAG} = get_user_id() -  called")
        
        user = self.db.query(Admin).filter(Admin.email == email).first()
        if user:
            return user.id
        else:
            return None


    def get_admins(self):
        logger.info(f"{TAG} = get_admins() -  called")
        admins = self.db.query(Admin).all()
        return admins


    def add_admin(self, admin: Admin):
        logger.info(f"{TAG} = add_admin() -  called")

        self.db.add(admin)
        self.db.commit()

        return admin


    def delete_admin(self, admin: Admin):
        logger.info(f"{TAG} = delete_admin() -  called")
        
        self.db.delete(admin)

        self.db.commit

    def get_market_name(self, admin_id:id):
        logger.info(f"{TAG} = delete_admin() -  called")

        # Keresés az adatbázisban az admin_id alapján
        admin = self.db.query(Admin).filter(Admin.id == admin_id).first()

        # Ha találtunk admin-t az adott admin_id-vel
        if admin:
            # Visszaadjuk az admin nevét
            return admin.market_name
        else:
            # Ha nem találtunk, akkor None-t adunk vissza
            return None


    # def get_refresh_token(self, refresh_token:str):
    #     logger.info(f"{TAG} = get_refresh_token() -  called")
    #     token = self.db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    #     return token


    # def add_refresh_token(self, refresh_token: RefreshToken):
    #     logger.info(f"{TAG} = add_refresh_token() -  called")

    #     self.db.add(refresh_token)
    #     self.db.commit()

    #     return refresh_token
