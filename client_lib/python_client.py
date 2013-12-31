#!/usr/bin/python

import json
import urllib
import urllib2

domain_name = "http://localhost:5000/"


def query(query):
    """
    json_query is a json dict with keys "input" and "output". The "input" value is a dict of inputs with keys as tags and values as the values of the tag, i.e. "zip": 61820. The "output" value is a dict of outputs with keys as the requested output (and also serves as a tag) and values as return types, i.e. "hour": "int".
    Example:
    json_query = {"action": "weather", "input": {"weather": 94539}, "output": {"temperature": "int"}}
    """
    data = urllib.urlencode(query)
    req = urllib2.Request(domain_name + "query?", data)
    response = urllib2.urlopen(req)

    if response:
        response = response.read()
        response = urllib2.unquote(response)
        response = json.loads(response)
        urls = response['apis']
        # print urls[0][0]
        responses = []
        for url in urls:
            responses.append(query_proxy(url[0], query))
        return decide(responses)
    else:
        return False


def query_proxy(url, query):
    """
    Goes to the proxy endpoints and returns each response from each proxy.
    """
    url += "?json=" + urllib2.quote(json.dumps(query))
    response = urllib2.urlopen(url).read()
    return response

def decide(response):
    """
    Iterates through all responses and returns the best response.
    Algorithm:
    - iterate through each output
    - find most common output
    - return that output
    """
    return response

# apropros.com/register_api?api_name=...&api_provider=...&api_url=...&provider_key=...&tag=...
def register_api(api_provider, api_name, api_url, provider_key, tags):
    """
    Allows an API provider to register an API.
    """
    url = domain_name + "register_api?"
    url += "api_name=" + api_name + "&api_provider=" + api_provider + "&provider_key=" + \
        provider_key + "&tags=" + \
        urllib2.quote(json.dumps(tags)) + \
        "&api_url=" + urllib2.quote(api_url)
    try:
        response = urllib2.urlopen(url)
    except:
        return False
    if response:
        print response.read()
        return True
    else:
        return False

# apropros.com/register_api_provider?api_provider=...&contact_info=...
def register_api_provider(api_provider, contact_info):
    """
    Register as an API provider.
    """
    url = domain_name + "register_api_provider?"
    url += "api_provider=" + api_provider + "&contact_info=" + contact_info
    try:
        response = urllib2.urlopen(url)
    except:
        return False
    if response:
        print response.read()
        return True 
    else:
        return False
print query(json.loads('{"action": "stocks", "input": {"stock_symbol": "BAC"}, "output": {"Volume": "float", "Days High" : "string"}}'))
#register_api_provider('https://127.0.0.1:8000','13917714J@gmail.com')
#register_api('https://127.0.0.1:8000', 'weather', '064dd4fd-b5c4-4e5c-9cb3-017fcc505032', ['weather','location','temperature','zip','city'])
# query_proxy("http://127.0.0.1:8000/query",json.loads('{"action": "weather", "input": {"location": "Bethesda"}, "output": {"temperature": "String"}}'))
#query(json.loads('{"action": "stocks", "input": {"stock_symbol": "BAC"}, "output": {"Volume": "float"}}'))
