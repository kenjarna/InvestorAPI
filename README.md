# InvestorAPI
Creating an investment API for data management

# Introduction
# Developers: Kenny Jarnagin(2019), 
#                Graham Wood(2019)
#                Collin Beauchamp-Umphrey(2019)

This was programmed in Python3, and uses SQLAlchemy and Flask in conjunction. Please ensure your computer has all three.

Furthermore, in order to use this program the user must have downloaded the iexfinance API onto their computer.

For information on how to do so, please look at https://addisonlynch.github.io/iexfinance/stable/install.html,
this program was created on the 0.3.5 version.

# API Documentation

The base route gives a printout of all stocks in the database, returning their ticker, price, open, close, and last update.
As such:

/
{<ticker>: {
  {
    'price'       : Some Number
    'open'        : Some Number
    'close'       : Some Number
    'Last Update' : Some Date
  }}
 {<someOtherTicker: ...}
                    
                    
Stocks can also be requested individually.

/<stockTicker>
  {
    'price'         : Some Number
    'open'          : Some Number
    'close'         : Some Number
    'Last Update'   : Some Date
    'Collection ID' : Some String
  }
  
 Finally stocks have a property called Collections that are the next level below them. Collections give more information on stocks. They can be inspected for a description
 
/<stockTicker>/<collectionID>
  {'id'          : Some name
   'description' : Some description
  }



