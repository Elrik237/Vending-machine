from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class DeclarativeBase:
    pass


DeclarativeBase = declarative_base(cls=DeclarativeBase)


class ListOfSnacks(DeclarativeBase):
    __tablename__ = 'snacks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    quantity = Column(Integer)

    def __init__(self, title, price, quantity):
        self.title = title
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return "<Snacks('%s','%s', '%s')>" % (
            self.title, self.price, self.quantity)

