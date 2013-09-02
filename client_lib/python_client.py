#!/usr/bin/python

import json
import urllib2

domain_name = "http://localhost:5000/"

def query(json_query):
	"""
	json_query is a json dict with keys "input" and "output". The "input" value is a dict of inputs with keys as tags and values as the values of the tag, i.e. "zip": 61820. The "output" value is a dict of outputs with keys as the requested output (and also serves as a tag) and values as return types, i.e. "hour": "int". 
	Example:
	json_query = {"input": {"zip": 61820, "day": "tuesday"}, "output": {"temperature": "int"}}
	"""
	url = domain_name + "query?json="
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
