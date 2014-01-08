#!/usr/bin/python

import json
import requests

domain_name = "http://localhost:5000/"


def query_proxy(content):
    """
    Returns response from proxy.
    """
    req = requests.post(content['url'] + '?json=',
                        data=json.dumps(content['query']),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    return response


def query(query, target=None, wisdom=100, fast=False):
    """
    Example:
    json_query = {"action": "weather",
                  "input": {"zip": 94539},
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
    response = req.json()

    if response:
        urls = [url[0] for url in response['apis']]
        contents = [{'url': url, 'query': query} for url in urls]

        if 'wisdom' in query["mode"]:
            if fast:  # Fast mode
                from multiprocessing import Process, Queue
                return
            elif target:  # Target mode
                return
            else:  # Wisdom mode
                from multiprocessing import Pool
                pool = Pool(len(urls) if len(urls) < wisdom else wisdom)
                response = pool.map(query_proxy, contents)
                return decide(response)

        return None
    else:
        return None


def register_api_provider(api_provider, contact_info):
    """
    Register as an API provider.
    """

    req = requests.post(domain_name + "register_api_provider?",
                        data=json.dumps({'api_provider': api_provider,
                                         'contact_info': contact_info}),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    return response


def register_api(api_provider, api_name, api_url,
                 provider_key, tags, api_login_info):
    """
    Allows an API provider to register an API.
    """

    req = requests.post(domain_name + "register_api?",
                        data=json.dumps({'api_provider': api_provider,
                                         'api_name': api_name,
                                         'api_url': api_url,
                                         'provider_key': provider_key,
                                         'tags': tags,
                                         'api_login_info': api_login_info,
                                         'category': 'test'}),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    return response

print query({"action": "stocks",
             "input": {"stock_symbol": "BAC"},
             "output": {"Volume": "float",
                        "Days High": "string"}})

# print register_api_provider('Google', 'google@gmail.com')

# print register_api("Google", "Stocks", "stocks.google.com",
#                    "123", ['stocks'], "idk")
