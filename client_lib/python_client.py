#!/usr/bin/python

import json
import urllib2

def query(json_query):
	url = "http://localhost:5000/query?"
	py_dict = json.loads(json_query)
	fields = [k for k, v in py_dict.items()]
	values = py_dict.values()
	dict_tuples = zip(fields, values)
	if len(fields) == len(values):
		for i, (field, value) in enumerate(dict_tuples):
			if i != len(dict_tuples) - 1:
				url += str(field) + "=" + str(value) + "&"
			elif i == len(dict_tuples) - 1:
				url += str(field) + "=" + str(value)
	response = urllib2.urlopen(url)
	return str(json.loads(str(response.read())))

print query(json.dumps({"weather": "null", "zip": 61820, "time": "now"}))
