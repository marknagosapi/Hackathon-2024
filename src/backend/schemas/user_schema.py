from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    points:int = 0
    level_id:int | None = None

class UserSchema(User):
    password: str
