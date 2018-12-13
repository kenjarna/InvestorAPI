from main import app, db
import json

session = db.session

print("################    DB TESTS    ###################")
assert(len(db.getStocks()) == 0)
#See if we can add a stock correctly
print("\t Testing addStock . . . ")
db.addStock(ticker='TSLA', collectionID = None)
assert(len(db.getStocks()) == 1)
assert(db.getStock('TSLA').ticker == 'TSLA')
assert(db.getStock('TsLA') is None)


#Get all stocks in DB
print("\t Testing getStocks . . .")
db.addStock(ticker='MSFT', collectionID = None)
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
db.addStock(ticker='TSLA', collectionID = None)
db.addStock(ticker='AAPL', collectionID = None)
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
db.addStock(ticker = 'TSLA', collectionID = None)
db.addStock(ticker = 'MSFT', collectionID = "Tech")

# Testing existing stock
print("\t Testing GET stock list . . .")
r = client.get('/')
assert(r.status_code == 200)
contents = get_json(r)

assert("stocks" in contents)
assert(len(contents["stocks"]) == 2)
assert('TSLA' in contents["stocks"][0])
assert('MSFT' in contents["stocks"][1])

#Get a specific collection in DB
print("\t Testing GET stock ticker . . .")
r = client.get('/MSFT')
contents = get_json(r)
assert(r.status_code == 200)
assert('MSFT' in contents["ticker"])

r = client.get('TSLA')
contents = get_json(r)
assert(r.status_code == 200)
assert('TSLA' in contents["ticker"])

#Create new stock
print("\t Testing PUT stock create . . .")
r = client.put('/TSLA')
assert(r.status_code == 403)
r = client.put('/MSFT')
assert(r.status_code == 403)
r = client.put('/AAPL')
assert(r.status_code == 201)

#Delete stock
print("\t Testing DELETE stock delete . . .")
r = client.delete('/TSLA')
assert(r.status_code == 204)
assert(len(db.getStocks()) == 2)
r = client.get('/MSFT')
assert(r.status_code == 200)
r = client.get('/AAPL')
assert(r.status_code == 200)
# r = client.delete('/TSLA')
# assert(r.status_code == 403)

db.addCollection('Tech', 'Tech stocks')
#Get Collection
print("\t Testing GET collection . . .")
r = client.get('/MSFT' + '/Tech')
assert(r.status_code == 200)
contents = get_json(r)
assert(contents['description'] == 'Tech stocks' and contents['id'] == 'Tech')
r = client.get('/MSFT')
assert(r.status_code == 200)
contents = get_json(r)
assert(contents['ticker'] == 'MSFT' and contents['collectionID'] == "Tech")

#Put collection
print("\t Testing PUT collection . . . ")
r = client.put('/ORCL'+ '/Magic' ,data=json.dumps({"description": "Magic"}), content_type='application/json')
assert(r.status_code == 201)
r = client.put('/GOOGL'+ '/Data Miners Welcome', data=json.dumps({"description": "Data Miners Unite"}), content_type='application/json')
assert(r.status_code == 201)
assert(len(db.getCollections()) == 3)


#Delete Collection
print("\t Testing DELETE collection . . . ")
r = client.delete('/ORCL' + '/Magic')
assert(r.status_code == 204)
assert(len(db.getCollections()) == 2)
assert(db.getCollection('/Magic') is None)
assert(db.getStock('ORCL') is  None)
assert(db.getStock('GOOGL') is None)
r = client.delete('/GOOGL'+'/Data Miners Welcome')
assert(len(db.getCollections()) == 1)

print("##############   API TESTS DONE   #################")
