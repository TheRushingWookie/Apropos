from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import inspect
from os.path import *
import sys

def run_proxy(proxy_name):
	global actions,json_outputs
	dir = os.path.abspath(inspect.getsourcefile(run_proxy))
	dir =  os.path.dirname(dir)
	sys.path.append(dir)
	mod = importlib.import_module("proxies." + proxy_name)

	print str(mod.__name__)
	try:
		proxy_instance = getattr(mod, proxy_name)()
		print proxy_instance.actions
		return proxy_instance
	except AttributeError:
		print 'function not found ' + "init_actions"

# instance = run_proxy('YahooStocks')
instance = run_proxy('WebServiceXStockQuotes')

@instance.interface.route("/query")
def query():
	immutable_multi_dict = request.args

	norm_dict = dict(immutable_multi_dict)


	io_json_list = norm_dict['json'][0]

	io_json_dict = json.loads(io_json_list)
	#return str(instance.actions)
    #io_json_dict = json.loads(io_json_dict)

	action = io_json_dict['action']

	print action
	if action:
		print(str(instance.actions))
		funct = instance.actions[str(action)]

		print str(funct)
		json_output =  funct(io_json_dict)
		return instance.filter_outputs(io_json_dict,json_output)
	return "hello"

if __name__ == "__main__":
    instance.interface.run(port=9000,debug=False)
    # instance.interface.run(port=8000,debug=False)
