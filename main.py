"""
    Developers: Kenny Jarnagin(2019), 
                Graham Wood(2019)
                Collin Beauchamp-Umphrey(2019)
"""

from flask import Flask, request, make_response, json, url_for, abort
from db import Db   # See db.py
from iexfinance import Stock #the API used to fetch stock data

app = Flask(__name__)
db = Db()
app.debug = True # Comment out when not testing
app.url_map.strict_slashes = False   # Allows for a trailing slash on routes

#### ERROR HANDLERS

@app.errorhandler(500)
def server_error(e):
   return make_json_response({ 'error': 'unexpected server error' }, 500)

@app.errorhandler(404)
def not_found(e):
   return make_json_response({ 'error': e.description }, 404)

@app.errorhandler(403)
def forbidden(e):
   return make_json_response({ 'error': e.description }, 403)

@app.errorhandler(400)
def client_error(e):
   return make_json_response({ 'error': e.description }, 400)

#Get Function for all stocks at the root level. Takes nothing, because it returns all stocks
@app.route('/', methods = ['GET'])
def stock_list():
    stocks = db.getStocks() #Call to get list of all stocks
    return make_json_response({ #Respond to user with below information
        "stocks": [{
                    stock.ticker: {"price": stock.price,
                               "open": stock.openPrice,
                               "close": stock.close,
                               "last update": stock.lastUpdate}}
            for stock in stocks #Do it for all stocks in stocks
        ]
        })


#GET function for an individual stock
@app.route('/<stockTicker>', methods = ['GET'])
def stock_data(stockTicker):
    stockTickerHelper(stockTicker) #Make sure that stock actually exists
    return make_json_response({ #Respond with below information
        "ticker": stockTicker,
        "price": db.getStock(stockTicker).price,
        "open": db.getStock(stockTicker).openPrice,
        "close": db.getStock(stockTicker).close,
        "last update": db.getStock(stockTicker).lastUpdate,
        "collectionID": db.getStock(stockTicker).collectionID
        })

#Adds new stocks to the list
@app.route('/<stockTicker>', methods = ['PUT'])
def stock_create(stockTicker):
    if db.getStock(stockTicker) is not None: #Lines to check to make sure no duplicates are created
        abort(403, "Stock already exists")
    db.addStock(stockTicker,None)
    db.commit()
    return make_json_response ({'Good': 'stock created'}, 201)

#Function Deletes a given stock
@app.route('/<stockTicker>', methods = ['DELETE'])
def stock_delete(stockTicker):
    if db.getStock(stockTicker) is None: #Check that the stock being deleted actually exists
        abort(403, "Stock does not exist")
    db.deleteStock(db.getStock(stockTicker))
    db.commit()
    return make_json_response({'Good': 'stock deleted'}, 204)


#GET for a specific collection
@app.route('/<stockTicker>/<collectionID>', methods = ['GET'])
def collection_data(stockTicker, collectionID):
    collectionIdHelper(collectionID) #Make Sure the Collection Exists
    return make_json_response({ #Return the following information to the user
        "id": collectionID,
        "description": db.getCollection(collectionID).description
        })

#Creates a new collection
@app.route('/<stockTicker>/<collectionID>', methods = ['PUT'])
def collection_create(stockTicker,collectionID):
    if db.getCollection(collectionID) is not None: #Check to Make sure the stock does not already exist
        abort(403, "Collection already exists")
    description = descriptionHelper()
    db.addCollection(collectionID, description)
    db.commit()
    return make_json_response({'Good':"collection created"}, 201)


@app.route('/<stockTicker>/<collectionID>', methods = ['DELETE'])
def collection_delete(stockTicker,collectionID):
    if db.getCollection(CollectionID) is None: #Check that the collection being deleted actually exists
        abort(403, "Collection does not exist")
    db.deleteCollection(db.getCollection(collectionID))
    db.commit()
    return make_json_response({'Good':"collection deleted"}, 204)


#Responds to user query
def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)

#Makes sure that a stck actually exists
def stockTickerHelper(ticker):
    stock = db.getStock(ticker)
    if stock == None:
        abort(404, "Stock not found")
    return stock

#Makes sure that a collection actually exists
def collectionIdHelper(id):
    collection = db.getCollection(id)
    if collection == None:
        abort(404, "Stockssssss not found")
    return collection

#Gets the description for the collection
def descriptionHelper():
   contents = request.get_json()
   if contents is None:
      abort(400)
   if "description" not in contents:
      description = None
   else: description = contents["description"]
   return description
