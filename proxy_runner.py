from flask import Flask, request
from os.path import *
import os
import sys
import json
import inspect
import importlib

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
        print proxy_instance.actions
        return proxy_instance
    except AttributeError:
        print 'function not found ' + "init_actions"

instance = run_proxy(sys.argv[1])  # YahooStocks, WebServiceXStockQuotes


@instance.interface.route("/query", methods=['POST'])
def query():
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == '/query'
    assert request.method == 'POST'

    action = request.json['action']

    if action:
        funct = instance.actions[str(action)]
        json_output = funct(request.json)

        return instance.filter_outputs(request.json, json_output)

if __name__ == "__main__":
    instance.interface.run(port=int(sys.argv[2]), debug=False)  # 8000, 9000
