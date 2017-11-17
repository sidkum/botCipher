# -*- coding: utf-8 -*-

# !/usr/bin/env python
# **********************************************
# *** Update or verify the following values. ***
# **********************************************



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

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "2f22ecfd9fa54027ba5976df791e98a7"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"



def giveResult(request):
    if len(subscriptionKey) == 32:
        term=request.get("result").get("resolvedQuery")
        print('Searching the Web for: ',term)
        headers, result = BingWebSearch(term)
        print("\nRelevant HTTP Headers:\n")
        print("\n".join(headers))
        print("\nJSON Response:\n")
        #print(json.dumps(json.loads(result), indent=4))
        data = json.dumps(json.loads(result), indent=4)
        res = createResponse(data,request)
        #print(res)
        return res
    else:
        print("Invalid Bing Search API subscription key!")
        print("Please paste yours into the source code.")


def BingWebSearch(search):
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


def createResponse(data,request):
    data=json.loads(data)
    webPages=data.get("webPages")#.get("value")
    val=webPages.get("value")
    return {"speech": "see this on messenger",
            "displayText": "see this on messenger",
            "data": {
                "facebook": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "list",
                            "top_element_style": "compact",
                            "elements": [
                                {
                                    "title": val[0].get("name"),
                                    "subtitle": val[0].get("snippet"),
                                    "image_url": "",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": val[0].get("url")
                                    }
                                },
                                {
                                    "title": val[1].get("name"),
                                    "subtitle": val[1].get("snippet"),
                                    "image_url": "",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": val[1].get("url")
                                    }
                                },
                                {
                                    "title": val[2].get("name"),
                                    "subtitle": val[2].get("snippet"),
                                    "image_url": "",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": val[2].get("url")
                                    }
                                },
                                {
                                    "title": val[3].get("name"),
                                    "subtitle": val[3].get("snippet"),
                                    "image_url": "",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": val[3].get("url")
                                    }
                                }],
                            "buttons": [
                                {
                                    "title": "More Results",
                                    "type": "web_url",
                                    "url":"https://www.google.co.in/search?source=hp&ei=hJIFWoO-I8rqvgTs3JzoBQ&q="+request.get("result").get("resolvedQuery")+"&oq=automata&gs_l=psy-ab.3...2003.3256.0.3406.10.7.0.0.0.0.0.0..0.0....0...1.1.64.psy-ab..10.0.0.0...0.oMuvqur__Fo"
                                }
                            ]
                        }}
                }}
}
