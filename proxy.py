
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
	def query(query_json)
