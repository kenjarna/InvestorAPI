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

#Test delete stock
db.deleteStock(db.getStock('TSLA'))
assert(len(db.getStocks()) == 1)
assert(db.getStock('MSFT') is not None)
assert(db.getStock('TSLA') is None)

#Test delete all stocks
db.addStock(ticker='TSLA')
db.addStock(ticker='AAPL')
assert(len(db.getStocks()) == 3)
db.deleteAllStocks()
assert(len(db.getStocks()) == 0)

print("################ DB TESTS DONE  ###################")
print("################   API TESTS   ###################")

# ADD YOUR API TESTS HERE
# ADD YOUR API TESTS HERE
client = app.test_client()
def get_json(r):
   return json.loads(r.get_data().decode("utf-8"))
db.addStock(ticker = 'TSLA')

# Testing existing stock
r = client.get('/')
assert(r.status_code == 200)
contents = get_json(r)

assert("stocks" in contents)
assert(len(contents["stocks"]) == 1)


print("##############   API TESTS DONE   #################")
