#!/usr/bin/python

import json
import urllib
import urllib2
from multiprocessing import Pool

domain_name = "http://localhost:5000/"


def query(query, target=None, wisdom=100, fast=False):
    """
    json_query is a json dict with keys "input" and "output". The "input" value is a dict of inputs with keys as tags and values as the values of the tag, i.e. "zip": 61820. The "output" value is a dict of outputs with keys as the requested output (and also serves as a tag) and values as return types, i.e. "hour": "int".
    Example:
    json_query = {"action": "weather", "input": {"weather": 94539}, "output": {"temperature": "int"}}
    """

    def query_proxy(url):
        """
        Goes to the proxy endpoints and returns each response from each proxy.
        """
        url += "?json=" + urllib2.quote(json.dumps(query))
        response = urllib2.urlopen(url).read()
        return json.loads(response)

    def decide(responses):
        """
        Iterates through all responses and returns the best response.
        Algorithm:
        - hash each response
        - find key with largest value
        - return the response corresponding to the key

        O(n) time with O(n) worst-case space
        """
        cache = dict()

        # Fill up the hash table
        for response in responses:
            cache[frozenset(response.items())] = cache.get(frozenset(response), 0) + 1

        # Find the most common response from the cache
        final_response, response_counter = None, 0
        for response in responses:
            if response_counter < cache[frozenset(response.items())]:
                response_counter = cache[frozenset(response.items())]
                final_response = response
        return final_response

    # Switch mode
    if isinstance(target, basestring):
        query["mode"] = {"target": target}
    elif isinstance(wisdom, int):
        query["mode"] = {"wisdom": wisdom}
    elif fast:
        query["mode"] = {"wisdom": 1}
    else:
        return None

    data = urllib.urlencode(json.loads(query))
    req = urllib2.Request(domain_name + "query?", data)

    # Retrieve IPs of proxies
    try:
        response = urllib2.urlopen(req)
    except Exception as e:
        print e

    if response:
        response = response.read()
        response = urllib2.unquote(response)
        response = json.loads(response)

        urls = [url[0] for url in response['apis']]

        if wisdom in query["mode"]:
            pool = multiprocessing.Pool(workers=wisdom) # how much parallelism?
            response = pool.map(query_proxy, urls)
            return decide(response)

<<<<<<< HEAD
        return None
    else:
        return None
=======
def decide(responses, target=False, wisdom=False):
    """
    Iterates through all responses and returns the best response.
    Algorithm:
    - hash each response
    - find key with largest value
    - return the response corresponding to the key
    """
    cache = dict()

    # Fill up the hash
    for response in responses:
        cache[frozenset(response.items())] = cache.get(frozenset(response), 0) + 1

    # Find the most common response from the cache
    final_response, response_counter = None, 0
    for response in responses:
        if response_counter < cache[frozenset(response.items())]:
            response_counter = cache[frozenset(response.items())]
            final_response = response
    return final_response
>>>>>>> 931f04bbb590a2372090300b0af601ca50956e47

# apropros.com/register_api?api_name=...&api_provider=...&api_url=...&provider_key=...&tag=...
def register_api(api_provider, api_name, api_url, provider_key, tags, api_login_info):
    """
    Allows an API provider to register an API.
    """
    url_dict = {'api_provider':api_provider,'api_name':api_name,'api_url':api_url,'provider_key':provider_key,'tags':tags,'api_login_info':api_login_info,'category':'test'}
    url = domain_name + "register_api?"
    url += urllib.urlencode(url_dict)
    print url
    try:
        response = urllib2.urlopen(url)
    except:
        return False
    if response:
        print response.read()
        return True
    else:
        return False

#register_api('Example_provider','test139','127.0.0.1:8000/test139','72e85cde-fba4-4456-b1e8-e26284d7d862',['no tags',],'''{"username":"Quinn","apikey":"123"}''')
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

# print query(json.loads('{"action": "stocks", "input": {"stock_symbol": "BAC"}, "output": {"Volume": "float", "Days High" : "string"}}'))
