import json
import copy
import requests
from multiprocessing import Pool, Process, Queue, active_children
from hashlib import sha1
import hmac
import base64
from collections import OrderedDict


domain_name = "http://localhost:5000/"
provider_key = '268aaf3f-5c50-45d3-bf8d-4134747e2420'


"""
Public library functions:
"""


def query(query, target=None, wisdom=100, fast=False):
    """
    Example:
    query = {"action": "weather",
             "input": {"zip": 94539},
             "output": {"temperature": "int"}}
    """

    if isinstance(target, basestring):
        query["mode"] = {"target": target}
    elif fast:
        wisdom = 1
        query["mode"] = {"wisdom": wisdom}
    elif isinstance(wisdom, int):
        query["mode"] = {"wisdom": wisdom}
    else:
        raise Exception("Invalid Mode")

    req = requests.post(domain_name + "query?",
                        data=json.dumps(query),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()

    if response:
        tag_map = response['corrected_tags']
        print query
        query = sanitize_tags(query, tag_map)
        print query
        urls = [url[0] for url in response['apis']]
        contents = [{'url': url, 'query': query} for url in urls]

        if 'wisdom' in query["mode"]:
            if fast:
                q = Queue(len(urls))

                def fast_wrapper(params):
                    q.put(query_proxy(params), block=False)

                # Fire off a process for each url
                processes = [Process(target=fast_wrapper, args=(content,))
                             for content in contents]
                [p.start() for p in processes]

                # Block until first process returns
                # and kill all other living processes
                fastest_response = q.get(block=True, timeout=60)

                # This is dirty. Will cause broken pipes
                # on proxy servers that did not return yet.
                [p.terminate() for p in active_children()]

                return sanitize_tags(fastest_response, tag_map)

            else:  # Wisdom mode
                print "urls returned %s" % (urls)
                pool = Pool(len(urls) if len(urls) < wisdom else wisdom)
                response = pool.map(query_proxy, contents)

                return decide(response)

        elif isinstance(target, basestring):
            return

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


def get_key_hmac(base_string):
    assert (provider_key)
    print base_string
    return base64.urlsafe_b64encode(hmac.new(provider_key,base_string,sha1).digest())


def hmac_json_string(json_input_unordered):
    json_input = OrderedDict(sorted(json_input_unordered.items(),key=lambda t: t[0]))
    hmac = get_key_hmac(json.dumps(json_input))
    json_input['hmac'] = hmac
    return json.dumps(json_input)


def register_api(api_provider, api_name, api_url,
                 provider_key, tags, api_login_info,category):
    """
    Allows an API provider to register an API.
    """
    json_text = hmac_json_string({'api_provider': api_provider,
                                         'api_name': api_name,
                                         'api_url': api_url,
                                         'tags': tags,
                                         'api_login_info': api_login_info,
                                         'category': category})
    print json_text
    req = requests.post(domain_name + "register_api?",
                        data=json_text,
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    return response


register_api('Example_provider','forecast','http://localhost:9000/query',"268aaf3f-5c50-45d3-bf8d-4134747e2420",('city','latitude','longitude','lat','lng','long','humidity', 'pressure', 'cloudiness', 'temperature', 'min_temp', 'current temperature', 'max_temp', 'speed', 'wind_direction'),"{}",'weather')


"""
Private helper functions begin below.
"""


def query_proxy(content):
    """
    Returns response from proxy.
    """
    try:
        req = requests.post(content['url'] + '?json=',
                            data=json.dumps(content['query']),
                            headers={'Content-type': 'application/json',
                                     'Accept': 'application/json'})
        response = req.json()
    except:
        return {'Status': False}
    return response


def sanitize_tags(query, tag_map):
    '''Adjust query to use tags in tag_map.'''
    standardized_query = copy.deepcopy(query)
    print "start %s" % (standardized_query)
    for tag in query['input']:
        standard_tag = tag_map[tag]
        standardized_query['input'][standard_tag] = query['input'][tag]
        #standardized_query['input'].pop(tag)
    for tag in query['output']:
        standard_tag = tag_map[tag]
        standardized_query['output'][standard_tag] = query['output'][tag]
        #standardized_query['output'].pop(tag)
    print "end %s" % (standardized_query)
    return standardized_query


# print sanitize_tags({'action': 'weather', 'input': {'citya': 'Urbana'}, 'mode': {'wisdom': 100}, 'output': {'temperatured': 'int'}},{u'city': u'citya', u'temperatured': u'temperature', u'citya': u'city', u'temperature': u'temperatured'})


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

    print responses
    # Fill up the hash table
    for response in responses:

        hashable_response = frozenset(response.items())
        if hashable_response in cache:
            cache[hashable_response] += 1
        else:
            cache[hashable_response] = 1

    # Find the most common response from the cache
    final_response, response_counter = None, 0
    for response in responses:
        if response_counter < cache[frozenset(response.items())]:
            response_counter = cache[frozenset(response.items())]
            final_response = response

    return final_response


'''
Some example calls
'''


if __name__ == "__main__":
     print query({"action": "weather",
                  "apikey": "4e6c3cb57748a14de046c4620ec9d7d7",
                  "input": {"latitude": "10", "longitude": '10'},
                  "output": {"temperature": "int", 'adadad' : 'int'}})

#     # print register_api_provider('Google', 'google@gmail.com')

#     # print register_api("Google", "Stocks", "stocks.google.com",
#     #                    "123", ['stocks'], "idk")
