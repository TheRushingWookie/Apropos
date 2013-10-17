#!/usr/bin/python

import json
import urllib2

domain_name = "http://localhost:5000/"

def query(query):
	"""
	json_query is a json dict with keys "input" and "output". The "input" value is a dict of inputs with keys as tags and values as the values of the tag, i.e. "zip": 61820. The "output" value is a dict of outputs with keys as the requested output (and also serves as a tag) and values as return types, i.e. "hour": "int". 
	Example:
	json_query = {"action": "weather", "input": {"weather": 94539}, "output": {"temperature": "int"}}
	"""
	url = domain_name + "query?action="
	input_url = ""
	output_url = ""
	action = query["action"]	

	inputs = query["input"].keys()
	for input_ in inputs:
		input_url += "&input=" + urllib2.quote(input_)

	outputs = query["output"].keys()
	for output_ in outputs:
		output_url += "&output=" + urllib2.quote(output_)

	url += action + input_url + output_url
	response = urllib2.urlopen(url)

	if response:
		print "Response is " + response.read()
	else:
		return False

# apropros.com/register_api?api_name=...&api_provider=...&api_url=...&provider_key=...&tag=...
def register_api(api_provider, api_name, api_url, provider_key, tags):
	url = domain_name + "register_api?"
	url += "api_name=" + api_name + "&api_provider=" + api_provider + "&provider_key=" + provider_key + "&tags=" + urllib2.quote(json.dumps(tags)) + "&api_url=" + urllib2.quote(api_url)
	try:
		response = urllib2.urlopen(url)
	except:
		return False
	if response:
		print response.read()
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
		print response.read()
		return True
	else:
		return False

#register_api_provider('https://127.0.0.1:8000','13917714J@gmail.com')
#register_api('https://127.0.0.1:8000', 'weather', '064dd4fd-b5c4-4e5c-9cb3-017fcc505032', ['weather','location','temperature','zip','city'])
# query(json.dumps('{"input": {"zip": 61820}, "output": {"temperature": "int"}}'))
