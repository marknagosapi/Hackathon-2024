from fastapi.security import OAuth2PasswordBearer
from config.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = SessionLocal()
