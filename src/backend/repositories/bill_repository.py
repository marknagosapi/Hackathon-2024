from models.admin import Admin
from models.item import Item
from models.bill import Bill
from sqlalchemy.orm import Session
from loguru import logger


TAG = "BillRepository"


class BillRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bill(self, bill: Bill):
        logger.info(f"{TAG} = create_bill() -  called")

        db_bill = Bill(**bill.dict())
        self.db.add(db_bill)
        self.db.commit()
        return db_bill
