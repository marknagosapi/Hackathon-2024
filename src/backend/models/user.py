from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    points = Column(Integer, default=0)
    level_id = Column(Integer,  ForeignKey('levels.id'))
    password = Column(String)
