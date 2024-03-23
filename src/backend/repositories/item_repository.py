from typing import List
from models.item import Item
from sqlalchemy.orm import Session
from loguru import logger

TAG = "ItemRepository"


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_items(self):
        logger.info(f"{TAG} = find_items() -  called")
        items = self.db.query(Item).all()
        return items

    def find_items_by_bill_id(self, bill_id:int):
        logger.info(f"{TAG} = find_item_by_id() -  called")
        items = self.db.query(Item).filter(Item.bill_id == bill_id).all()
        return items



    def create_item(self, item: Item):
        logger.info(f"{TAG} = create_item() -  called")

        db_item = Item(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        return db_item
    

    def create_items(self, items: List[Item]):
        logger.info(f"{TAG} = create_items() -  called")
        
        # item_list = [item.model_dump() for item in items]

        results = self.db.add_all(items)
        self.db.commit()
        return items
