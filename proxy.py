
from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import inspect
from os.path import *
import sys
interface = Flask(__name__)
actions = {}

@interface.route("/query")
def query():

	
	immutable_multi_dict = request.args
	
	norm_dict = dict(immutable_multi_dict)
	
	io_json_list = norm_dict['json']
	
	io_json_dict = json.loads(io_json_list[0])
	io_json_dict = json.loads(io_json_dict)
	io_json_dict = json.loads(io_json_dict)
	action = io_json_dict['action']
	print action
	if action:
		print(str(actions))
		funct_name = actions[action]
		print str(funct_name)
		funct = get_funct(funct_name[1],funct_name[0])
		print str(funct)
		return funct(io_json_dict)
def run_proxy(proxy_name):
	global actions
	dir = os.path.abspath(inspect.getsourcefile(run_proxy))
	dir =  os.path.dirname(dir)
	
	mod = importlib.import_module("proxies." + proxy_name)
	print str(mod.__name__)
	try:
		func = getattr(mod, "init_actions")
		actions = func()
		
	except AttributeError:
		print 'function not found ' + "init_actions"
	

def get_funct(funct_name,package_name):
	try:
		func = getattr(sys.modules[package_name], funct_name)
	except AttributeError:
		print 'function not found ' + funct_name
	else:
		return func

if __name__ == "__main__":
	run_proxy('openweathermap')
	print str(actions)
	interface.run(port=8000)

