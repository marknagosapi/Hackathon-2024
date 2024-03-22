from pydantic import BaseModel
from datetime import date

class Admin(BaseModel):
    first_name: str
    last_name: str
    email: str
    market_name:str

class AdminSchema(Admin):
    password: str
