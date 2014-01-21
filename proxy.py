
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

	def __init__ (self):
		pass
	def standard_type_converter(self,val,val_type):
		'''Converts all standard types such as integer, string'''
		val_type = val_type.lower()
		print "val_type " + val_type + ' ' + str(val)
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