from flask import Flask, request
from os.path import *
import os
import sys
import json
import inspect
import importlib
import logging
from random import randint
from multiprocessing import Process
"""
Usage:
python proxy_runner.py YahooStocks 8000;
python proxy_runner.py WebServiceXStockQuotes 9000
"""
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

proxies = {}

def run_proxy(proxy_name):
    global actions, json_outputs 
    directory = os.path.abspath(inspect.getsourcefile(run_proxy))
    directory = os.path.dirname(directory)
    sys.path.append(directory)
    mod = importlib.import_module("proxies." + proxy_name)

    print str(mod.__name__)

    proxy_instance = getattr(mod, proxy_name)()
    print proxy_instance
    actions = proxy_instance.init_actions()
    return proxy_instance
logger = None
for proxy_name in ["openweathermap"]:#"WebServiceXStockQuotes"]:
    proxies[proxy_name] = run_proxy(proxy_name)  # YahooStocks, WebServiceXStockQuotes
    if not logger:
        logger = proxies[proxy_name].interface.logger

def start_proxy(**kwargs):
    print kwargs['proxy'].api_name
    print kwargs['port']
    kwargs['proxy'].interface.run(port=kwargs['port'])

if __name__ == "__main__":
    for proxy_name in proxies:
        proxy = proxies[proxy_name]
        p = Process(target=start_proxy, kwargs={'proxy':proxy,'port':proxy.port})
        p.start()
        #proxy.interface.run(port=proxy.port,debug=True)
    #    instance.interface.run(port=int(7000), debug=True)  # 8000, 9000
