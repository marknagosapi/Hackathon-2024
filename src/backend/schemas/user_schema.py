from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id:int | None = None
    first_name: str
    last_name: str
    email: str
    points:int = 0
    level_id:int | None = None

class UserSchema(User):
    password: str
