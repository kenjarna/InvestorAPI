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

#The principle class for the API
class Stock(Base):
    __tablename__ = 'stocks'
    ticker = Column(String(6), nullable=False,primary_key=True) # A String that is a short form of a company name
    price = Column(Integer, nullable=False) #An integer for the price of a stock
    openPrice = Column(Integer, nullable=False) #The price of the stock the morning of the current day
    close = Column(Integer, nullable=False) #The price of the stock at the end of the last day
    lastUpdate = Column(DateTime(), default = datetime.now()) #Last time the information has been requested
    collectionID = Column(String, ForeignKey("collections.id", ondelete="CASCADE"), default = "None") #What collection is the stoc a part of?

    collections = relationship("Collection",back_populates="stocks")

    def __repr__(self):
        return "Stock<%s %s %s %s %s>" % (self.ticker,self.price,self.openPrice,self.close, self.lastUpdate)

class Collection(Base):
    __tablename__ = 'collections'
    id = Column(String, nullable=False,primary_key=True) #Name of the Collection
    description = Column(String) #A short description
 
    stocks = relationship("Stock", back_populates='collections')

    def __repr__(self):
        return "Collection<%s %s>" %(self.id, self.description)


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

        #Gets All Stocks in the current db
    def getStocks(self):
        return self.session.query(Stock).all()

    #Gets a single stock in the current db
    def getStock(self, ticker):
        return self.session.query(Stock)\
                 .filter_by(ticker=ticker)\
                 .one_or_none()

    #Introduces a new stock to the db, only needs a ticker and a collectionID(can be None)
    def addStock(self, ticker, collectionID):
        stock = Stock(ticker=ticker,
                      price = st(ticker).get_price(),
                      openPrice = st(ticker).get_open(), 
                      close = st(ticker).get_close(),
                      collectionID = collectionID)
        self.session.add(stock)
        return stock    

    #Deletes a given stoc from the database
    def deleteStock(self, stock):
        self.session.delete(stock)

        #deletes all stocks from the database. Currently unused
    def deleteAllStocks(self):
        for stock in self.getStocks():
            self.session.delete(stock)

            #Gets an individual collection
    def getCollection(self, id):
        return self.session.query(Collection)\
                .filter_by(id=id)\
                .one_or_none()

    #Gets all collections
    def getCollections(self):
        return self.session.query(Collection).all()

    #Introduces a new Collection to the db
    def addCollection(self, id, description):
        collection = Collection(id=id, description=description)
        self.session.add(collection)
        return collection

    #Deletes a collection, given that collection
    def deleteCollection(self, collection):
        self.session.delete(collection)

        #deletes all collections. Currently Unused
    def deleteAllCollections(self):
        for collection in self.getCollections():
            self.session.delete(collection)
