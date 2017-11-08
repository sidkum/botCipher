# -*- coding: utf-8 -*-

#!/usr/bin/env python
# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "2f22ecfd9fa54027ba5976df791e98a7"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "iphoneX"

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
import http.client, urllib.parse, json

# Flask app should start in global layout
app = Flask(__name__)
 
@app.route('/webhook', methods=['POST'])

def giveResult(request):
    if len(subscriptionKey) == 32:
        print('Searching the Web for: ', "iphoneX")
        headers, result = BingWebSearch(term)
        print("\nRelevant HTTP Headers:\n")
        print("\n".join(headers))
        print("\nJSON Response:\n")
        data =json.dumps(json.loads(result), indent=4)
        res = createResponse(data)
        return res
    else:
        print("Invalid Bing Search API subscription key!")
        print("Please paste yours into the source code.")



def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    print("\nSearch Url: ")
    print(conn.request)
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")
   
def createResponse(data):
    val=data.get("value")
    return {"name":"see this on messenger",
	    "displayText":"see this on messenger",
	    "data": {
             "facebook": {
             "attachment": {
	    "type":"template",
            "payload":{
             "template_type":"list",
	     "top_element_style": "compact",
            "elements":[
            {
             "title": val[0].get("name"),
             "subtitle": val[0].get("snippet"),
             "image_url":"",          
	     "default_action": {
               "type": "web_url",
               "url": val[0].get("url")
              }
	    },
	     {
             "title": val[1].get("name"),
             "subtitle": val[1].get("snippet"),
             "image_url":"",          
	     "default_action": {
               "type": "web_url",
               "url": val[1].get("url")
              }
	    },
            {
             "title": val[2].get("name"),
             "subtitle": val[2].get("snippet"),
             "image_url":"",          
	     "default_action": {
               "type": "web_url",
               "url": val[2].get("url")
              }
	    },
            {
             "title": val[3].get("name"),
             "subtitle": val[3].get("snippet"),
             "image_url":"",          
	     "default_action": {
               "type": "web_url",
               "url": val[3].get("url")
              }
	    }],
      	"buttons": [
          {
            "title": "Read More",
            "type": "postback",
            "payload": "read more" 
	  }
        ] 
      }}
	}}
}
if __name__ == '__main__':
   port = int(os.getenv('PORT', 5000))
   print("Starting app on port %d" % port)
   app.run(debug=True, port=port, host='0.0.0.0')
