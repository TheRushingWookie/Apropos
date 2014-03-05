from flask import Flask, request
from os.path import *
import os
import sys
import json
import inspect
import importlib
import logging

"""
Usage:
python proxy_runner.py YahooStocks 8000;
python proxy_runner.py WebServiceXStockQuotes 9000
"""
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Headers'] = "Origin, X-Requested-With,Content-Type, Accept"
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def run_proxy(proxy_name):
    global actions, json_outputs 
    directory = os.path.abspath(inspect.getsourcefile(run_proxy))
    directory = os.path.dirname(directory)
    sys.path.append(directory)
    mod = importlib.import_module("proxies." + proxy_name)

    print str(mod.__name__)
    try:
        proxy_instance = getattr(mod, proxy_name)()
        print proxy_instance
        actions = proxy_instance.init_actions()
        return proxy_instance
    except AttributeError:
        print 'function not found ' + "init_actions"

instance = run_proxy("openweathermap")  # YahooStocks, WebServiceXStockQuotes
logger = instance.interface.logger

@instance.interface.route("/query", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def query():

    io_json_dict = request.json
    #return str(instance.actions)
    #io_json_dict = json.loads(io_json_dict)
    logger.debug('Json is %s', io_json_dict)
    action = io_json_dict['action']
    print action
    if action:
        print(str(instance.actions))
        funct = instance.actions[str(action)]

        logger.debug("Funct selected is %s", str(funct))
        json_output =  funct(io_json_dict)
        logger.debug("json_output %s", str(json_output))
        callback = request.args.get('callback')
        if callback:
            return '{0}({1})'.format(callback, instance.filter_outputs(io_json_dict,json_output))
        else: return instance.filter_outputs(io_json_dict,json_output)
    return "hello"  

if __name__ == "__main__":
    instance.interface.run(port=int(7000), debug=True)  # 8000, 9000
