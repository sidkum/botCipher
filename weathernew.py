# !/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit

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

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecastNew":
        return {}
    data = json.loads(result)
    
    
    data = YahooWeather(APP_ID="8eqyZg6s",
                     api_key="dj0yJmk9dkw3YWVLTEdXUmNRJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTM3",
                     api_secret="fd427dd3ec3da0046fbd78ac1444f1a660259c6d")
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    
    data.get_yahoo_weather_by_city('city', Unit.celsius)
    print(data.condition.text)
    print(data.condition.temperature)
    res = makeWebhookResult(data)

    data.get_yahoo_weather_by_location(35.67194, 51.424438)
    print(data.condition.text)
    print(data.condition.temperature)
    return res

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + data.condition.get('text') + \
             ", the temperature is " + data.condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')


                     
