import requests
import json

# input = {'stock_symbol': 'BAC'}


def yahoo_stocks_api(input):
    url = 'http://query.yahooapis.com/v1/public/yql? \
           q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol in ('
    for key in input:
        if key == 'stock_symbol':
            for symbol in input[key]:
                url += '"' + symbol + '",'

    url += "%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org \
            %2Falltables.env&format=json"
