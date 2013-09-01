#!/usr/bin/python

from flask import Flask
from flask import request
import json
import email_script
import database

# Create flask object
interface = Flask(__name__)

# apropros.com/query
@interface.route("/query")
def web_query():
	try:
		tags = dict(request.args)
		return str(request.args)
	except:
		return json.dumps({'Status': False})

# apropros.com/register_api_provider/<api_provider_name>?contact_info=...
@interface.route("/register_api_provider/<api_provider>")
def web_register_api_provider(api_provider):
	'''
	To-do:
		- check if valid email
		- check if no other html parameters entered
		- add rate limiter
	'''
	try:
		contact_info_string = str(dict(request.args)["contact_info"][0])
		registration_key = database.register_api_provider(api_provider, contact_info_string)
		if registration_key:
			email_script.send_email("13917714j", "3019236Q", "13917714j@gmail.com", contact_info_string, registration_key)
			return json.dumps({'Status': True})
		else:
			return json.dumps({'Status': False})
	except:
			return json.dumps({'Status': False})

# apropros.com/register_api/<api_name>&tag=...
@interface.route("/register_api/<api_name>")
def web_register_api(api_name):
	try:
		# Returns all values that have "tag" as the key
		return str(str(api_name) + str(dict(request.args)["tag"]))
	except:
		return json.dumps({'Status': False})

# apropros.com/drop_api/<api_name>
@interface.route("/drop_api/<api_name>")
def web_drop_api(api_name):
	try:
		# sqlite implementation to be implemented
		return "Delete " + api_name + " from the database"
	except:
		return json.dumps({'Status': False})

if __name__ == "__main__":
	interface.run()
