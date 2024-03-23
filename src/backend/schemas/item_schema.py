from pydantic import BaseModel


class ItemSchema(BaseModel):
    name: str
    quantity: int
    unique_price: float 
    total_price: float | None = None

class ItemInDb(ItemSchema):
    bill_id:int | None = None