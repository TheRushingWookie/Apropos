#!/usr/bin/python

from flask import Flask
from flask import request
import json
import email_script
import database
import urllib2

# Create flask object
interface = Flask(__name__)

# def uumd_to_list(umd, key):
# 	# converts unicode UnmutableMultiDict to a list
# 	unicode_list = list(dict(uumd)[key])
# 	list = []
# 	for item in list:
# 		list.append(str(item))
# 	return list

# apropros.com/query
@interface.route("/query")
def web_query():
	try:
		tags_unicode = list(dict(request.args)["tag"])
		tags = []
		for tag in tags_unicode:
			tags.append(str(tag))
		return str(database.query_api(tags))
	except:
		return json.dumps({"Status": False})

# apropros.com/register_api_provider?api_provider=...&contact_info=...
@interface.route("/register_api_provider")
def web_register_api_provider():
	"""
	To-do:
		- check if valid email
		- check if no other html parameters entered
		- add rate limiter
	"""
	try:
		api_provider = str(dict(request.args)["api_provider"][0])
		contact_info_string = str(dict(request.args)["contact_info"][0])
		registration_key = database.register_api_provider(api_provider, contact_info_string)
		if registration_key:
			email_script.send_email("13917714j", "3019236Q", "13917714j@gmail.com", contact_info_string, registration_key)
			return json.dumps({"Status": True})
		else:
			return json.dumps({"Status": False})
	except:
			return json.dumps({"Status": False})

# apropros.com/register_api?api_name=...&api_provider=...&provider_key=...&tag=...
@interface.route("/register_api")
def web_register_api():
	try:
		api_name = urllib2.unquote(str(list(dict(request.args)["api_name"])[0]))
		api_provider = str(list(dict(request.args)["api_provider"])[0])
		provider_key = str(list(dict(request.args)["provider_key"])[0])
		tags_unicode = list(dict(request.args)["tag"])
		tags = []
		for tag in tags_unicode:
			tags.append(str(tag))
		if database.add_api_endpoint(api_provider, api_name, provider_key, tags):
			return json.dumps({"Status": True})
		else:
			return json.dumps({"Status": False})
	except:
		return json.dumps({"Status": False})

# apropros.com/drop_api?api_name=...
@interface.route("/drop_api")
def web_drop_api():
	try:
		api_name = str(list(dict(request.args)["api_name"])[0])
		return "Delete " + api_name + " from the database"
	except:
		return json.dumps({"Status": False})

if __name__ == "__main__":
	interface.run()
