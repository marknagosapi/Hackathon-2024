from sqlalchemy import Column, Integer, String, ForeignKey, Double
from config.database import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('bills.id'))
    name = Column(String)
    quantity = Column(Integer)
    unique_price = Column(Double)
    total_price = Column(Double)
