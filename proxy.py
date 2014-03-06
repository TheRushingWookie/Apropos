
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
import requests

class proxy():
	interface = Flask(__name__)
	logger = interface.logger
	output_tag_paths = []
	provider_key = ''
	provider_name = ''
	domain_name = "http://localhost:5000/"
	api_name = ''
	tags = []
	input_tags = []
	config_file_path = os.getcwd() + "/json_config.json"
	#update_tags(api_provider_name,api_endpoint_name,owner_key,new_tags)
	def load_config(self):
		'''Loads a json config file to provide initialization values for provider_key, provider_name, domain_name, api_name.'''
		with open(self.config_file_path, 'r') as json_file:
			json_string = json_file.read()
			json_config = json.loads(json_string)
			print json_config
			self.provider_key = json_config['provider_key']
			self.provider_name = json_config['provider_name']
			self.domain_name = json_config['domain_name']
			self.api_name = json_config['api_name']
	def write_config(self):
		'''Writes a json config file which includes provider_key, provider_name, domain_name, api_name.'''
		with open(self.config_file_path, 'w') as json_file:
			json_data = {'provider_key':self.provider_key,'provider_name':self.provider_name,'domain_name':self.domain_name,'api_name':self.api_name}
			json_file.write(json.dumps(json_data, json_file, indent=4))
			json.dumps(json_data,json_file)
	def __init__ (self):
		self.actions = self.init_actions()
		self.json_outputs = self.init_outputs()
		self.logger.debug(self.json_outputs)
		tags = self.output_tag_paths.keys() + self.input_tags
		self.load_config()
		self.update_tags(self.tags)
	
			


	def standard_type_converter(self,val,val_type):
		'''Converts all standard types such as integer, string'''
		val_type = val_type.lower()
		self.logger.debug( "val_type " + val_type + ' ' + str(val))
		try:
			if val_type == 'int' or val_type == 'integer':
				if val.find('.'):
					return int(float(val))	
				return int(val)
			elif val_type == 'string':
				return str(val)
			elif val_type == 'float':
				return float(val)
		except:
			print "Bad conversion of " + str(val) + " + with type " + str(val_type) #  Might want to make str(val) keep escaped characters
		return val
	def custom_type_converter(self,val,val_type):
			'''Stub function to let conversions of individuation'''
			return val
	def filter_outputs (self,json_input,output):
		'''Filters the output of an api into what is requested and makes sure the data conforms to SI Units'''
		filtered_json = {}

		for i in json_input['output'].keys():

			try:
				funct = self.json_outputs[i]

				self.logger.debug(self.json_outputs)
				converted_val = funct(output,i)
				#print "Filterd " + converted_val
				filtered_json[i] = self.standard_type_converter(converted_val,json_input['output'][i])
				#print "Filterd " + str(type(filtered_json[i]))
				filtered_json[i] = self.custom_type_converter(filtered_json[i],json_input['output'][i])
				#print "Filterd 2 " + str(type(filtered_json[i]))
				#print str(type(converted_val))
			except Exception,e:
				self.logger.debug(str(e))
				return str(traceback.format_exc())
				return json.dumps({'wrong_outputs':i})
		return json.dumps(filtered_json)
	def update_tags(self,tags):
		payload = {'api_provider':self.provider_name,'provider_key':self.provider_key,'api_name':self.api_name,'tags':self.tags}
		headers = {'content-type': 'application/json'}
		r = requests.post(self.domain_name + 'update_tags',data=json.dumps(payload),headers=headers)
	def query_access_funct(self,json_output,field):
		path = self.output_tag_paths[field]
		self.logger.debug("path %s", path)
		self.logger.debug("field %s",field)
		self.logger.debug('json_output %s', json_output)
		if json_output != None:
			for i in path:
				if i in json_output:
					json_output = json_output[i]
				else:
					self.logger.debug('Path to %s is messed up. %s ',i,json_output)
					return "Path to json field is messed up"
			return json_output
		else:
			return "Null"


	def init_outputs(self):
		field_names = self.output_tag_paths
		field_funct_hash = {}
		name_conversions = {}
		self.logger.debug("fields %s ",field_names)
		for key in field_names.keys():
			field_funct_hash[key] = self.query_access_funct

		return field_funct_hash
	def init_actions(self):
		return None
	def get_funct(self,funct_name,package_name):
		try:
			func = getattr(sys.modules[package_name], funct_name)
		except AttributeError:
			print 'function not found ' + funct_name
		else:
			return func