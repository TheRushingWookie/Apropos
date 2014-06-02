import json
import copy
import requests
from multiprocessing import Pool, Process, Queue, active_children
from hashlib import sha1
import hmac
import base64
from collections import OrderedDict
import logging

domain_name = "http://localhost:5000/"
provider_key = '268aaf3f-5c50-45d3-bf8d-4134747e2420'
logger = logging.getLogger('PythonClient')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

"""
Public library functions:
"""


def query(query, mode='wisdom', target=None, wisdom=100):
    """
    Example:
    query = {"action": "weather",
             "input": {"zip": 94539},
             "output": {"temperature": "int"}}
    """
    print "in"
    logger.debug('start')

    req = requests.post(domain_name + "query?",
                        data=json.dumps(query),
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    logger.debug('query %s', query)
    if response:
        tag_map = response['corrected_tags']

        query = sanitize_tags(query, tag_map)
        logger.debug('response json %s', response)
        urls = response['apis']
        contents = [{'url': url, 'query': query} for url in urls]
        logger.debug('urls %s', contents)
        if mode == 'fast':
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
        elif mode == 'target' and target != None:
            logger.debug('Target mode for %s', target)
            target_contents = select_target(target, contents)
            logger.debug('Target query %s' % target_contents)
            return query_proxy(target_contents)
        else:  # Wisdom mode
            logger.debug("urls returned %s" % (urls))
            pool = Pool(len(urls) if len(urls) < wisdom else wisdom)
            response = pool.map(query_proxy, contents)

            return decide(response)
        return None
    else:
        return None

def select_target(target, contents_list):
    for contents in contents_list:
        if contents['url'][1] == target:
            return contents
    raise ValueError('No target found. Possible targets: %s' % contents_list)
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
    req = requests.post(domain_name + "register_api?",
                        data=json_text,
                        headers={'Content-type': 'application/json',
                                 'Accept': 'application/json'})
    response = req.json()
    return response


register_api('Example_provider','forecast','http://localhost:9000/query',"268aaf3f-5c50-45d3-bf8d-4134747e2420",('city','latitude','longitude','lat','lng','long','humidity', 'pressure', 'cloudiness', 'temperature', 'min_temp', 'current temperature', 'max_temp', 'speed', 'wind_direction'),"{}",'weather')

register_api('Example_provider','mailgun','http://localhost:10000/query',"268aaf3f-5c50-45d3-bf8d-4134747e2420",("",),"{}",'sendmail')


"""
Private helper functions begin below.
"""


def query_proxy(content):
    """
    Returns response from proxy.
    """
    try:
        req = requests.post(content['url'][0] + '?json=',
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
    for tag in query['input']:
        standard_tag = tag_map[tag]
        standardized_query['input'][standard_tag] = query['input'][tag]
        #standardized_query['input'].pop(tag)
    for tag in query['output']:
        standard_tag = tag_map[tag]
        standardized_query['output'][standard_tag] = query['output'][tag]
        #standardized_query['output'].pop(tag)
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
     print query({"action": "sendmail",
                  "apikey": "key-3kjoic9aj4qio1d8luw4sw1morxis465",

                  "input": {"from": "sandboxc7032282a60b4700ab4a0c433421cbc5.mailgun.org",
                            "to": 'quinnjarr@gmail.com',
                            "subject" : "testing",
                            "text" : "helloworld"},
                  "output": {"message" : "string"}},target='mailgun', mode='target')

#     # print register_api_provider('Google', 'google@gmail.com')

#     # print register_api("Google", "Stocks", "stocks.google.com",
#     #                    "123", ['stocks'], "idk")
