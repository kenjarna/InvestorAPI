"""
	Developers: Kenny Jarnagin(2019), 
				Graham Wood(2019)
				Collin Beauchamp-Umphrey(2019)
"""

from flask import Flask, request, make_response, json, url_for, abort
from db import Db   # See db.py
import utils
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
def stock():
	pass