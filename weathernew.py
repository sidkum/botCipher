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
    if req.get("result").get("action") != "yahooWeatherForecastNew":
        return {}
    apiKey = e8fa3ad8df464a83d97c6e9d9b0a3ff5
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    yql_url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&units=metric&appid="+apiKey
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    query = data.get("weather")
    if query is None:
        speech = "query element missing from news's response"
        return createResponse(speech, speech,data)
    city = data.get("city")
    forecast = data.get("weather")[0].get("main")
    tempr = data.get("main").get("temp")
    # print(json.dumps(item, indent=4))

    speech = "Today in " + city + ": " +forecast+ \
             ", the temperature is " + tempr + "celsius"
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')


                     
