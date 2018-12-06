from main import app, db
import json

session = db.session

print("################    DB TESTS    ###################")
assert(len(db.getStocks()) == 0)
#See if we can add a stock correctly
db.addStock(ticker='TSLA')
assert(len(db.getStocks()) == 1)
assert(db.getStock('TSLA').ticker == 'TSLA')
assert(db.getStock('TsLA') is None)
#Get all stocks in DB
db.addStock(ticker='MSFT')
assert(len(db.getStocks()) == 2)
assert(db.getStock('TSLA') is not None)
assert(db.getStock('MSFT') != db.getStock('TSLA'))
print(db.getStocks())
print("################ DB TESTS DONE  ###################")
