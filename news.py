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
    if req.get("result").get("action") != "news.search":
        speech = "Invalid Action specified"
        return createResponse(speech, speech)
    yql_url = "https://newsapi.org/v1/articles?source=the-times-of-india&apiKey=6614fb3731b2472c9efa015800e01de3"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    #return {
#	"speech":data.get("status"),
#	"displayText":data.get("source")
 #   	}
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    query = data.get("articles")
    if query is None:
        speech = "query element missing from news's response"
        return createResponse(speech, speech,imageUrl,data)
    from random import randint
    i=randint(0,6)
    title = data.get("articles")[i].get("title")
    descrip = data.get("articles")[i].get("description")
    newsurl=data.get("articles")[i].get("url")
    urltoimage=data.get("articles")[i].get("urlToImage")
    #if (title is None) or (description is None):
    #    speech = "Hmm! Looks like we could not fetch the news"
   # else:
    speech = "\n"+"Title: " + title +"\n\n"+ "Description: " + descrip+"\n\n"+"Read in detail here:"+newsurl
    
    # print(json.dumps(item, indent=4))

##    print("speech=")
##    print(speech)
##    print("---------------")
##    print(createResponse(speech, speech))
##    print("------XXXX-----")

    return createResponse(speech, speech,urltoimage,data)

def createResponse(speech, displayText,data):
    from random import randint
    i=randint(0,5) 
    title=data.get("articles")[i].get("title")
    urltoimage=data.get("articles")[i].get("urlToImage")
    newsurl=data.get("articles")[i].get("url")
    return {"speech":speech,
	    "displayText":displayText,
	    "data": {
              "facebook": {
                "attachment": {
	       "type":"template",
            "payload":{
             "template_type":"generic",
            "elements":[
            {
             "title":title,
             "image_url":urltoimage
	    # "default_action": {
            # "type": "web_url",
            # "url":newsurl
            #}
             }]
      }}}}}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
