"""
    Developers: Kenny Jarnagin(2019), 
                Graham Wood(2019)
                Collin Beauchamp-Umphrey(2019)
"""

# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from iexfinance import Stock as st #API to fetch stock data
from datetime import datetime, timedelta
import json

Base = declarative_base()

class Stock(Base):
   __tablename__ = 'stocks'
   # TODO Will need to add the fields for the Bucket class here
   ticker = Column(String(6), nullable=False,primary_key=True)
   price = Column(Integer, nullable=False)
   openPrice = Column(Integer, nullable=False)
   close = Column(Integer, nullable=False)
   lastUpdate = Column(DateTime(), default = datetime.now())

   def __repr__(self):
      return "Stock<%s %s %s %s %s>" % (self.ticker,self.price,self.openPrice,self.close, self.lastUpdate)


# Represents the database and our interaction with it
class Db:
    def __init__(self):
        engineName = 'sqlite:///test.db'   # Uses in-memory database
        self.engine = create_engine(engineName)
        self.metadata = Base.metadata
        self.metadata.bind = self.engine
        self.metadata.drop_all(bind=self.engine)
        self.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def getStocks(self):
        return self.session.query(Stock).all()

    def getStock(self, ticker):
        return self.session.query(Stock)\
                 .filter_by(ticker=ticker)\
                 .one_or_none()

    def addStock(self, ticker):
        stock = Stock(ticker=ticker,
                      price = st(ticker).get_price(),
                      openPrice = st(ticker).get_open(), 
                      close = st(ticker).get_close())
        self.session.add(stock)
        return stock    

    def deleteStock(self, stock):
        self.session.delete(stock)

    def deleteAllStocks(self):
        for stock in self.getStocks():
            self.session.delete(stock)