from models.bill import Bill
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta

from loguru import logger


TAG = "BillRepository"


class BillRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_bills(self, user_id:int):
        logger.info(f"{TAG} = find_bills() -  called")
        bills = self.db.query(Bill).filter(Bill.user_id == user_id).all()
        return bills
    
    def find_all(self):
        logger.info(f"{TAG} = find_all() -  called")
        bills = self.db.query(Bill).all()
        return bills

    def find_bill_by_id(self, id:int):
        logger.info(f"{TAG} = find_bill_by_id() -  called")
        bill = self.db.query(Bill).filter(Bill.id == id).first()
        return bill
    
    def find_current_bill(self, user_id:int):
        logger.info(f"{TAG} = find_current_bill() -  called")

        earliest_bill = self.db.query(Bill).filter(Bill.user_id == user_id).order_by(desc(Bill.date)).first()

        if earliest_bill:
            if earliest_bill.date >= datetime.now() - timedelta(minutes=5):
                return earliest_bill
            else:
                logger.info("The earliest bill is older than 5 minutes.")
                return None
        else:
            return None

    def create_bill(self, bill: Bill):
        logger.info(f"{TAG} = create_bill() -  called")

        db_bill = Bill(**bill.dict())
        self.db.add(db_bill)
        self.db.commit()
        return db_bill
