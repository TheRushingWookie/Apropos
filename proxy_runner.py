from os.path import *
from multiprocessing import Process
import os
import sys
import inspect
from flask.ext.cors import *
import importlib
import logging
from logging import FileHandler
proxies = {}


def run_proxy(proxy_name):
    global actions, json_outputs
    directory = os.path.abspath(inspect.getsourcefile(run_proxy))
    directory = os.path.dirname(directory)
    sys.path.append(directory)
    mod = importlib.import_module("proxies." + proxy_name)

    proxy_instance = getattr(mod, proxy_name)(mod.__name__)
    print 'loggers %s' % logging.getLogger().manager.loggerDict.keys()
    actions = proxy_instance.init_actions()
    return proxy_instance


proxy_list = ["mailgun", ]
for proxy_name in proxy_list:
    # YahooStocks, WebServiceXStockQuotes
    proxies[proxy_name] = run_proxy(proxy_name)

def start_proxy(**kwargs):
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

            #logger = proxy.logger
