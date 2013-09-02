#!/usr/bin/python

import json
import urllib2

domain_name = "http://localhost:5000/"

def query(json_query):
	"""
	json_query is a json dict with values "input" and "output". "input" is a dict of inputs, "output" is a dict of outputs
	"""
	url = domain_name + "query?"
	try:
		encoded_query = urllib2.quote(json.dumps(json_query))
	if encoded_query:
		url += encoded_query
	else:
		return False
	try:
		response = urllib2.urlopen(url)
	except:
		return False
	if response:
		return str(json.loads(str(response.read())))
	else:
		return False

# apropros.com/register_api?api_name=...&api_provider=...&provider_key=...&tag=...
def register_api(api_provider, api_name, provider_key, tags):
	url = domain_name + "register_api?"
	url += "api_name=" + api_name + "&api_provider=" + api_provider + "&provider_key=" + provider_key + ""
	try:
		response = urllib2.urlopen(url)
	except:
		return False
	if response:
		return True
	else:
		return False

# apropros.com/register_api_provider?api_provider=...&contact_info=...
def register_api_provider(api_provider, contact_info):
	url = domain_name + "register_api_provider?"
	url += "api_provider=" + api_provider + "&contact_info=" + contact_info
	try:
		response = urllib2.urlopen(url)
	except:
		return False
	if response:
		return True
	else:
		return False

print query(json.dumps({"weather": "null", "zip": 61820, "time": "now"}))
