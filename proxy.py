
from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import traceback
import inspect
from os.path import *
import sys

class proxy():
	interface = Flask(__name__)
	actions = {}
	json_outputs = {}

	

	def standard_type_converter(self,val,val_type):
		
		if val_type == 'int':
			return int(val)
		elif val_type == 'string':
			return str(val)
		elif val_type == 'float':
			return float(val)
		return val
	def custom_type_converter(self,val,val_type):
		return None
	def filter_outputs (self,json_input,output):
		filtered_json = {}
		
		for i in json_input['output'].keys():

			try:
				funct = self.json_outputs[i]

				
				converted_val = funct(output)

				filtered_json[i] = self.standard_type_converter(converted_val,json_input['output'][i])
				filtered_json[i] = self.custom_type_converter(converted_val,json_input['output'][i])
			except Exception,e:
				print str(e)
				return str(traceback.format_exc())
				return json.dumps({'wrong_outputs':i})
		return json.dumps(filtered_json)

	
		

	def get_funct(self,funct_name,package_name):
		try:
			func = getattr(sys.modules[package_name], funct_name)
		except AttributeError:
			print 'function not found ' + funct_name
		else:
			return func

