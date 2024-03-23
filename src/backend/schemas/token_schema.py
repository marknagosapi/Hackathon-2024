import datetime
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str

class TokenData(BaseModel):
    email: str | None = None

class TokenCreationalData(BaseModel):
    sub: str
    exp: datetime.datetime
