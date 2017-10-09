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
    if req.get("result").get("action") != "newslive":
        speech = "Invalid Action specified"
        return createResponse(speech, speech)

    
    yql_url = "https://newsapi.org/v1/articles?source=cnn&apiKey=6614fb3731b2472c9efa015800e01de3"
    
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    query = data.get('status')
    if query is None:
        speech = "query element missing from news's response"
        return createResponse(speech, speech)
    else:
	speech = "data ok"
	return createResponse(speech, speech)
	
    #title = quote.get(['articles'][0]['title']);
    
    #description = quote.get(['articles'][0]['description']);
    
    
    #if (title is None) or (description is None):
    #    speech = "Hmm! Looks like we could not fetch the news"
    #else:
     #   speech = "Title: " + title + " description: " + description
	
    # print(json.dumps(item, indent=4))

##    print("speech=")
##    print(speech)
##    print("---------------")
##    print(createResponse(speech, speech))
##    print("------XXXX-----")

    #return createResponse(speech, speech)

def createResponse(speech, displayText):
##    print("Response:")
##    print (speech)
    return {
        "speech": speech,
        "displayText": displayText,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-news-org"
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
