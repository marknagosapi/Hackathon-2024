from sqlalchemy import Column, Integer, DateTime, ForeignKey, Double
from config.database import Base


class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    admin_id = Column(Integer, ForeignKey('admins.id'))
    date = Column(DateTime)
    item_number = Column(Integer)
    total = Column(Double)
   