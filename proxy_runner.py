from os.path import *
from random import randint
from multiprocessing import Process
from flask import request
import os
import sys
import inspect
import importlib


proxies = {}


def run_proxy(proxy_name):
    global actions, json_outputs
    directory = os.path.abspath(inspect.getsourcefile(run_proxy))
    directory = os.path.dirname(directory)
    sys.path.append(directory)
    mod = importlib.import_module("proxies." + proxy_name)

    print str(mod.__name__)

    proxy_instance = getattr(mod, proxy_name)(mod.__name__)
    print proxy_instance
    actions = proxy_instance.init_actions()
    return proxy_instance


proxy_list = ["openweathermap", ]
logger = None
for proxy_name in proxy_list:
    # YahooStocks, WebServiceXStockQuotes
    proxies[proxy_name] = run_proxy(proxy_name)
    if not logger:
        logger = proxies[proxy_name].logger


def start_proxy(**kwargs):
    print kwargs['proxy'].api_name
    print kwargs['port']
    kwargs['proxy'].run(port=kwargs['port'])


if __name__ == "__main__":
    for proxy_name in proxies:
        proxy = proxies[proxy_name]
        if len(proxy_list) > 1:
            p = Process(target=start_proxy,
                        kwargs={'proxy': proxy,
                                'port': proxy.port})
            p.start()

        else:
            proxy.run(port=proxy.port, debug=True)
