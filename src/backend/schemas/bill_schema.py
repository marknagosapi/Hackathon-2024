from typing import List
from pydantic import BaseModel
from schemas.item_schema import ItemSchema

class BillInDb(BaseModel):
    user_id: int 
    admin_id: int
    item_number: int | None = None
    total: float | None = None

class BillSchema(BillInDb):
    items: List[ItemSchema] = []
