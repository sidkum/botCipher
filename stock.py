#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "stockquote":
        speech = "Invalid Action specified"
        return createResponse(speech, speech)

    result = req.get("result")
    parameters = result.get("parameters")
    symbol = parameters.get("symbol")
    print("symbol=" + symbol)
    if symbol is None:
        speech = "What is the symbol?"
        return createResponse(speech, speech)
    
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(symbol)

    if yql_query is None:
        speech = "Error creating Yahoo query"
        return createResponse(speech, speech)
    
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(symbol):
    return "use 'http://www.datatables.org/yahoo/finance/quote/yahoo.finance.quote.xml' as t1;  select Symbol, Name, LastTradePriceOnly from t1 where symbol='"\
		+ symbol + "'"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        speech = "query element missing from Yahoo's response"
        return createResponse(speech, speech)

    result = query.get('results')
    if result is None:
        speech = "query/results element missing from Yahoo's response"
        return createResponse(speech, speech)

    quote = result.get('quote')
    if quote is None:
        speech = "query/results/quote element missing from Yahoo's response"
        return createResponse(speech, speech)

    price = quote.get('LastTradePriceOnly')
    name = quote.get('Name')
    symbol = quote.get('Symbol')

##    print("price=")
##    print(price)
##    print("name=")
##    print(name)
##    print("symbol=")
##    print(symbol)
    
    if (price is None) or (name is None) or (symbol is None):
        speech = "Hmm! Looks like the symbol was not found"
    else:
        speech = "Last price for " + symbol + " (" + name + ") was $" + price
	
    # print(json.dumps(item, indent=4))

##    print("speech=")
##    print(speech)
##    print("---------------")
##    print(createResponse(speech, speech))
##    print("------XXXX-----")

    return createResponse(speech, speech)

def createResponse(speech, displayText):
##    print("Response:")
##    print (speech)
    return {
        "speech": speech,
        "displayText": displayText,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-yahoo-stock-quote"
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
