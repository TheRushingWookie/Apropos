
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
	json_output_name_map = {} # This converts a input name to the api specific name. temperature -> current_temperature
	json_name_to_path_map = {} #converts api_specific name to the appropriate path within the output json. 

	def standard_type_converter(self,val,val_type):
		'''Converts all standard types such as integer, string'''
		val_type = val_type.lower()
		print "val_type " + val_type + ' ' + str(val)
		if val_type == 'int' or val_type == 'integer':

			return int(val)
		elif val_type == 'string':
			return str(val)
		elif val_type == 'float':
			return float(val)
		return val
	def custom_type_converter(self,val,val_type):
		''
		return val
	def filter_outputs (self,json_input,output):
		'''Filters the output of an api into what is requested and makes sure the data conforms to SI Unites'''
		filtered_json = {}
		
		for i in json_input['output'].keys():

			try:
				funct = self.json_outputs[i]

				#print funct
				converted_val = funct(output,i)
				#print "Filterd " + converted_val
				filtered_json[i] = self.standard_type_converter(converted_val,json_input['output'][i])
				#print "Filterd " + str(type(filtered_json[i]))
				filtered_json[i] = self.custom_type_converter(filtered_json[i],json_input['output'][i])
				#print "Filterd 2 " + str(type(filtered_json[i]))
				#print str(type(converted_val))
			except Exception,e:
				print str(e)
				return str(traceback.format_exc())
				return json.dumps({'wrong_outputs':i})
		return json.dumps(filtered_json)

	def query_access_funct(self,json_output,field):
		field = self.json_output_name_map[field]
		path = self.json_name_to_path_map[field]
		print str(json_output)
		#print field + str(json_output['query']['results']['quote'][field])
		print type(json_output)

		if json_output != None:
			for i in path:
				if i in json_output:
					json_output = json_output[i]
				else:
					return "Path to json field is messed up"
			return json_output
		else:
			return "Null"

		
	def init_outputs(self):

		field_names = self.json_output_name_map
		field_funct_hash = {}
		name_conversions = {}
		for key in field_names.keys():
			field_funct_hash[key] = self.query_access_funct

		return field_funct_hash
	def get_funct(self,funct_name,package_name):
		try:
			func = getattr(sys.modules[package_name], funct_name)
		except AttributeError:
			print 'function not found ' + funct_name
		else:
			return func

