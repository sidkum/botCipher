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
    if req.get("result").get("action") != "search.album":
        speech = "Invalid Action specified"
        return createResponse(speech, speech,data)
    yql_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=c68de8a6159c02cd683804aa40debc53&artist="+req.get("result").get("parameters").get("music-artist")+"&album="+req.get("result").get("parameters").get("music-album")+"&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    #return {
#	"speech":data.get("status"),
#	"displayText":data.get("source")
 #   	}
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    query = data.get("album")
    if query is None:
        speech = "query element missing from music response"
        return createResponse(speech, speech,data)
    #if (title is None) or (description is None):
    #    speech = "Hmm! Looks like we could not fetch the news"
   # else:
    #speech=" "
    speech=data.get("album").get("tracks").get("track")[0].get("name")
    #for i in range(0,9):
        #songname=data.get("toptracks").get("track")[i].get("name")
        #speech=speech+songname+"\n"
    # print(json.dumps(item, indent=4))

##    print("speech=")
##    print(speech)
##    print("---------------")
##    print(createResponse(speech, speech))
##    print("------XXXX-----")

    return createResponse(speech, speech,data)

def createResponse(speech, displayText,data):
##    print("Response:")
##    print (speech)
    #topsongs=data.get("toptracks").get("track")
    topsongs=data.get("album").get("tracks").get("track")[0].get("name")
    return {"speech":speech,
	    "displayText":displayText
	  '''  "data": {
             "facebook": {
             "attachment": {
	    "type":"template",
            "payload":{
             "template_type":"generic",
            "elements":[
            {
             "title": data.get("album").get("name"),
             "subtitle": data.get("album").get("wiki").get("wiki").get("content"),
             "image_url":data.get("album").get("image")[5].get("#text"),          
	     "default_action": {
               "type": "web_url",
               "url": data.get("album").get("url"),
              }
	    }]
      }}
	}}'''
}
 #   return {"speech":speech,
#	    "displayText":displayText,
#	    
 #  }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
