from main import app, db
import json

session = db.session

print("################    DB TESTS    ###################")
assert(len(db.getStocks()) == 0)
#See if we can add a stock correctly
print("\t Testing addStock . . . ")
db.addStock(ticker='TSLA')
assert(len(db.getStocks()) == 1)
assert(db.getStock('TSLA').ticker == 'TSLA')
assert(db.getStock('TsLA') is None)


#Get all stocks in DB
print("\t Testing getStocks . . .")
db.addStock(ticker='MSFT')
assert(len(db.getStocks()) == 2)
assert(db.getStock('TSLA') is not None)
assert(db.getStock('MSFT') != db.getStock('TSLA'))

#Test delete stock
print("\t Testing deleteStock . . .")
db.deleteStock(db.getStock('TSLA'))
assert(len(db.getStocks()) == 1)
assert(db.getStock('MSFT') is not None)
assert(db.getStock('TSLA') is None)

#Test delete all stocks
print("\t Testing deleteAllStocks . . .")
db.addStock(ticker='TSLA')
db.addStock(ticker='AAPL')
assert(len(db.getStocks()) == 3)
db.deleteAllStocks()
assert(len(db.getStocks()) == 0)

#Here, we begin tests for the collection class
print("\t Testing addCollection . . .")
assert(len(db.getCollections()) == 0)
#Test create collection
db.addCollection(id="Graham's Collection",description="Basic stuff")
assert(len(db.getCollections()) == 1)
assert(db.getCollection("Graham's Collection").description == "Basic stuff")

#Get all collections in DB
print("\t Testing getCollections . . .")
db.addCollection(id="Collin's Collection",description="Advanced stuff")
assert(len(db.getCollections()) == 2)
assert(db.getCollection("Collin's Collection").description == "Advanced stuff")
assert(db.getCollection("Graham's Collection") is not None)

#Test delete collection
print("\t Testing deleteCollection . . .")
db.deleteStock(db.getCollection("Graham's Collection"))
assert(len(db.getCollections()) == 1)
assert(db.getCollection("Graham's Collection") is None)
assert(db.getCollection("Collin's Collection") is not None)

#Test delete all collections
print("\t Testing deleteAllCollections . . .")
db.addCollection(id="Kenny's Collection", description="Is this done yet?")
assert(len(db.getCollections())==2)
db.deleteAllCollections()
assert(len(db.getCollections())==0)


print("################ DB TESTS DONE  ###################")
print("################   API TESTS   ###################")

# ADD YOUR API TESTS HERE
# ADD YOUR API TESTS HERE
client = app.test_client()
def get_json(r):
   return json.loads(r.get_data().decode("utf-8"))
db.addStock(ticker = 'TSLA')

# Testing existing stock
print("\t Testing existing stock . . .")
r = client.get('/')
assert(r.status_code == 200)
contents = get_json(r)

assert("stocks" in contents)
assert(len(contents["stocks"]) == 1)

assert('TSLA' in contents["stocks"][0]["ticker"])



print("##############   API TESTS DONE   #################")
