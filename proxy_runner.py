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

@instance.interface.route("/query", methods=['POST'])
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
        return instance.filter_outputs(io_json_dict,json_output)
    return "hello"  

if __name__ == "__main__":
    instance.interface.run(port=int(7000), debug=True)  # 8000, 9000
