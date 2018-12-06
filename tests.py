from main import app, db
import json

session = db.session

assert(len(db.getStocks()) == 0)

