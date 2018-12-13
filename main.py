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

@app.route('/', methods = ['GET'])
def stock_list():
    stocks = db.getStocks()
    return make_json_response({
        "stocks": [{
                    stock.ticker: {"price": stock.price,
                               "open": stock.openPrice,
                               "close": stock.close,
                               "last update": stock.lastUpdate}}
            for stock in stocks
        ]
        })



@app.route('/<stockTicker>', methods = ['GET'])
def stock_data(stockTicker):
    stockTickerHelper(stockTicker)
    return make_json_response({
        "ticker": stockTicker,
        "price": db.getStock(stockTicker).price,
        "open": db.getStock(stockTicker).openPrice,
        "close": db.getStock(stockTicker).close,
        "last update": db.getStock(stockTicker).lastUpdate
        })


@app.route('/<stockTicker>', methods = ['PUT'])
def stock_create(stockTicker):
    if db.getStock(stockTicker) is not None:
        abort(403, "Stock already exists")
    db.addStock(stockTicker)
    db.commit()
    return make_json_response ({'Good': 'bucket_created'}, 201)


@app.route('/<stockTicker>', methods = ['DELETE'])
def stock_delete(stockTicker):
    db.deleteStock(db.getStock(stockTicker))
    db.commit()
    return make_json_response({}, 204)



@app.route('/<stockTicker>/<collectionID>', methods = ['GET'])
def collection_data(collectionId):
    collectionIdHelper(collectionId)
    return make_json_response({
        "id": collectionId,
        "description": db.getCollection(collectionId).description
        })


@app.route('/<stockTicker>/<collectionID>', methods = ['PUT'])
def collection_create(collectionId):
    if db.getCollection(collectionId) is not None:
        abort(403, "Collection already exists")
    description = descriptionHelper()
    db.addCollection(collectionId, description)
    db.commit()
    return make_json_response({'Good':"collection created"}, 201)


@app.route('/<stockTicker>/<collectionID>', methods = ['DELETE'])
def collection_delete(collectionId):
    db.deleteCollection(db.getCollection(collectionId))
    db.commit()
    return make_json_response({'Good':"collection deleted"}, 204)



def make_json_response(content, response = 200, headers = {}):
   headers['Content-Type'] = 'application/json'
   return make_response(json.dumps(content), response, headers)

def stockTickerHelper(ticker):
    stock = db.getStock(ticker)
    if stock == None:
        abort(404, "Stock not found")
    return stock

def collectionIdHelper(id):
    collection = db.getCollection(id)
    if collection == None:
        abort(404, "Stock not found")
    return collection

def descriptionHelper():
   contents = request.get_json()
   if contents is None:
      abort(400)
   if "description" not in contents:
      description = None
   else: description = contents["description"]
   return description