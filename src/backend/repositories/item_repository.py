from typing import List
from models.item import Item
from sqlalchemy.orm import Session
from loguru import logger

TAG = "ItemRepository"


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db


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
