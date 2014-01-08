#!/usr/bin/python

import json
import urllib
import urllib2
import requests
from multiprocessing import Pool

domain_name = "http://localhost:5000/"


def query_proxy(content):
    """
    Returns response from proxy.
    """
    url = content['url']
    query = content['query']
    url += "?json=" + urllib2.quote(json.dumps(query))
    response = urllib2.urlopen(url).read()
    return json.loads(response)


def query(query, target=None, wisdom=100, fast=False):
    """
    json_query is a json dict with keys "input" and "output".
    The "input" value is a dict of inputs with keys as tags
    and values as the values of the tag, i.e. "zip": 61820.
    The "output" value is a dict of outputs with keys as the
    requested output (and also serves as a tag) and values as
    return types, i.e. "hour": "int".
    Example:
    json_query = {"action": "weather",
                  "input": {"weather": 94539},
                  "output": {"temperature": "int"}}
    """

    def decide(responses):
        """
        Iterates through all responses and returns the best response.
        Algorithm:
        1. hash each response for O(1) retrieval
        2. find key with largest value
        3. return the response corresponding to the key

        O(n) time with O(n) worst-case space
        """
        cache = dict()

        # Fill up the hash table
        for response in responses:
            cache[frozenset(response.items())] = cache.get(
                frozenset(response), 0) + 1

        # Find the most common response from the cache
        final_response, response_counter = None, 0
        for response in responses:
            if response_counter < cache[frozenset(response.items())]:
                response_counter = cache[frozenset(response.items())]
                final_response = response
        return final_response

    if isinstance(target, basestring):
        query["mode"] = {"target": target}
    elif isinstance(wisdom, int):
        query["mode"] = {"wisdom": wisdom}
    elif fast:
        query["mode"] = {"wisdom": 1}
    else:
        raise Exception("Invalid Mode")

    req = requests.post(domain_name + "query?",
                        data=json.dumps(query),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()  # Retrieve proxy endpoints

    if response:
        urls = [url[0] for url in response['apis']]
        contents = [{'url': url, 'query': query} for url in urls]
        if 'wisdom' in query["mode"]:
            pool = Pool(len(urls) if len(urls) <= wisdom else wisdom)
            response = pool.map(query_proxy, contents)
            return decide(response)

        return None
    else:
        return None


def register_api(api_provider, api_name, api_url,
                 provider_key, tags, api_login_info):
    """
    Allows an API provider to register an API.
    """
    url_dict = {'api_provider': api_provider,
                'api_name': api_name,
                'api_url': api_url,
                'provider_key': provider_key,
                'tags': tags,
                'api_login_info': api_login_info,
                'category': 'test'}

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


print query({"action": "stocks",
             "input": {"stock_symbol": "BAC"},
             "output": {"Volume": "float",
                        "Days High": "string"}})
