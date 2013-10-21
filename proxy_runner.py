from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import inspect
from os.path import *
import sys
def run_proxy(proxy_name):
	global actions,json_outputs
	dir = os.path.abspath(inspect.getsourcefile(run_proxy))
	dir =  os.path.dirname(dir)
	sys.path.append(dir)
	mod = importlib.import_module("proxies." + proxy_name)

	print str(mod.__name__)
	try:
		proxy_instance = getattr(mod, proxy_name)()
		print proxy_instance.actions
		

		return proxy_instance
	except AttributeError:
		print 'function not found ' + "init_actions"
instance = run_proxy('openweathermap')


@instance.interface.route("/query")
def query():
	immutable_multi_dict = request.args
	print "WBFJWEFBWJBFJBWFBWJFBWBFW"
	norm_dict = dict(immutable_multi_dict)

	
	io_json_list = norm_dict['json'][0]
	
	io_json_dict = json.loads(io_json_list)
	#return str(instance.actions)
    #io_json_dict = json.loads(io_json_dict)

	action = io_json_dict['action']

	print action
	if action:
		print(str(instance.actions))
		funct = instance.actions[action]

		print str(funct)
		raw_output =  funct(io_json_dict)
		return instance.filter_outputs(io_json_dict,json.loads(raw_output))
	return "hello"	
if __name__ == "__main__":
	
	'''
	print proxy_instance.filter_outputs(json.loads('{"output": {"temperature": "string","pressure":"string", "windspeed":"int"}}'),json.loads"""{
    "coord": {
        "lon": -77.0969,
        "lat": 38.9864
    },
    "sys": {
        "country": "United States of America",
        "sunrise": 1381835926,
        "sunset": 1381876149
    },
    "weather": [
        {
            "id": 801,
            "main": "Clouds",
            "description": "few clouds",
            "icon": "02d"
        }
    ],
    "base": "gdps stations",
    "main": {
        "temp": 292.808,
        "temp_min": 292.708,
        "temp_max": 292.708,
        "pressure": 1027.29,
        "sea_level": 1034.89,
        "grnd_level": 1027.29,
        "humidity": 71
    },
    "wind": {
        "speed": 1.95,
        "deg": 42.5005
    },
    "clouds": {
        "all": 20
    },
    "dt": 1381865209,
    "id": 4348599,
    "name": "Bethesda",
    "cod": 200
}"""))'''
	
	instance.interface.run(port=8000,debug=True)



