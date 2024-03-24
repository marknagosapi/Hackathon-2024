from sqlalchemy import Column, Integer, String
from config.database import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email = Column(String)
    market_name = Column(String)