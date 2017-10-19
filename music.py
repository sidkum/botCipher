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
    if req.get("result").get("action") != "searchmusic":
        speech = "Invalid Action specified"
        return createResponse(speech, speech)
    yql_url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="+req.get("result").get("parameters").get("music-artist")+"&api_key=c68de8a6159c02cd683804aa40debc53&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    #return {
#	"speech":data.get("status"),
#	"displayText":data.get("source")
 #   	}
    res = makeWebhookResult(data)
    return res




def makeWebhookResult(data):
    query = data.get("toptracks")
    if query is None:
        speech = "query element missing from news's response"
        return createResponse(speech, speech)
    #if (title is None) or (description is None):
    #    speech = "Hmm! Looks like we could not fetch the news"
   # else:
    speech=" "
    for i in range(0,9):
        songname=data.get("toptracks").get("track")[i].get("name")
        speech=speech+songname+"\n"
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
    toptracks=data.get("toptracks").get("track")
    return {
	"speech":speech,
	"displayText":displayText
	"data": {
           "facebook": {
             "attachment": {
	     "type":"template",
             "payload":{
             "template_type":"generic",
             "elements":[
            {
             "title": toptracks[0].get("name"),
             "subtitle": toptracks[0].get("url"),
             "image_url":toptracks[0].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[0].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[0].get("url")
              }
             ]
            },
           {
             "title": toptracks[1].get("name"),
             "subtitle": toptracks[1].get("url"),
             "image_url":toptracks[1].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[1].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[1].get("url")
              }
             ]
            },
          {
             "title": toptracks[2].get("name"),
             "subtitle": toptracks[2].get("url"),
             "image_url":toptracks[2].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[2].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[2].get("url")
              }
             ]
            },
		{
		     "title": toptracks[3].get("name"),
		     "subtitle": toptracks[3].get("url"),
		     "image_url":toptracks[3].get("image")[3].get("#text"),          
			"default_action": {
			"type": "web_url",
			"url": toptracks[3].get("url")
			},
		     "buttons": [
		      {
			"title": "View",
			"type": "web_url",
			"url": toptracks[3].get("url")
		      }
		     ]
		    },
	   {
             "title": toptracks[4].get("name"),
             "subtitle": toptracks[4].get("url"),
             "image_url":toptracks[4].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[4].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[4].get("url")
              }
             ]
            },
	  {
             "title": toptracks[5].get("name"),
             "subtitle": toptracks[5].get("url"),
             "image_url":toptracks[5].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[5].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[5].get("url")
              }
             ]
            },
	   {
             "title": toptracks[6].get("name"),
             "subtitle": toptracks[6].get("url"),
             "image_url":toptracks[6].get("image")[3].get("#text"),          
		"default_action": {
                "type": "web_url",
                "url": toptracks[6].get("url")
                },
             "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": toptracks[6].get("url")
              }
             ]
            }
          ]
      }}
     }}
	#"imageUrl":imageUrl
        # "data": data,
        # "contextOut": [],
        #"source": "apiai-news-org"
   }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
