from sqlalchemy import Column, Integer, String
from config.database import Base

class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    min_points = Column(Integer)
    max_points = Column(Integer)
    