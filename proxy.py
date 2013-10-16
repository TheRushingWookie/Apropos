
from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import inspect
from os.path import *
import sys

class proxy():
	interface = Flask(__name__)
	actions = {}
	json_outputs = {}

	@interface.route("/query")
	def query(self):

		
		immutable_multi_dict = request.args
		
		norm_dict = dict(immutable_multi_dict)
		
		io_json_list = norm_dict['json']
		
		io_json_dict = json.loads(io_json_list[0])
		io_json_dict = json.loads(io_json_dict)
		
		action = io_json_dict['action']
		print actions
		if action:
			print(str(self.actions))
			funct = self.actions[action]
			
			print str(funct)
			return funct(io_json_dict)
	def filter_outputs (self,json_input,output):
		filtered_json = {}

		for i in json_input['output'].keys():
			print json_outputs[i]
			try:
				funct = json_outputs[i]

				print funct
				filtered_json[i] = funct(output,json_input['output'][i])
			except:
				return json.dumps({'wrong_outputs':i})
		return json.dumps(filtered_json)

	
		

	def get_funct(self,funct_name,package_name):
		try:
			func = getattr(sys.modules[package_name], funct_name)
		except AttributeError:
			print 'function not found ' + funct_name
		else:
			return func
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
if __name__ == "__main__":
	proxy_instance = run_proxy('openweathermap')
	proxy_instance.get_weather()
	proxy_instance.interface.run(port=8000)


