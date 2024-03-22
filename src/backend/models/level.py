from sqlalchemy import Column, Integer, String
from config.database import Base

class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    min_points = Column(Integer)
    name = Column(String)