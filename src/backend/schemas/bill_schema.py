from typing import List
from pydantic import BaseModel
from schemas.item_schema import ItemSchema
import datetime

class BillInDb(BaseModel):
    user_id: int 
    admin_id: int
    date:datetime.datetime | None = None
    item_number: int | None = None
    total: float | None = None

class BillSchema(BillInDb):
    items: List[ItemSchema] = []
