from typing import List
from pydantic import BaseModel
from schemas.item_schema import ItemSchema

class BillSchema(BaseModel):
    user_id: int 
    admin_id: int
    item_number: int | None = None
    total: float | None = None
    items: List[ItemSchema] = []

