from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserSchema(User):
    password: str
