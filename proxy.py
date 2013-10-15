
from flask import Flask
from flask import request
import json
import urllib2
import importlib
import os
import inspect
from os.path import *
import sys
interface = Flask(__name__)
actions = {}
json_outputs = {}
@interface.route("/query")
def query():

	
	immutable_multi_dict = request.args
	
	norm_dict = dict(immutable_multi_dict)
	
	io_json_list = norm_dict['json']
	
	io_json_dict = json.loads(io_json_list[0])
	io_json_dict = json.loads(io_json_dict)
	
	action = io_json_dict['action']
	print actions
	if action:
		print(str(actions))
		funct_name = actions[action]
		print str(funct_name)
		funct = get_funct(funct_name[1],funct_name[0])
		print str(funct)
		return funct(io_json_dict)
def filter_outputs (json_input,output):
	filtered_json = {}

	for i in json_input['output'].keys():
		print json_outputs[i]
		try:
			funct = json_outputs[i]

			print funct
			filtered_json[i] = funct(output,json_input['output'][i])
		except:
			return json.dumps({'wrong_outputs':i})
	return json.dumps(filtered_json)

def run_proxy(proxy_name):
	global actions,json_outputs
	dir = os.path.abspath(inspect.getsourcefile(run_proxy))
	dir =  os.path.dirname(dir)
	
	mod = importlib.import_module("proxies." + proxy_name)
	print str(mod.__name__)
	try:
		func = getattr(mod, "init_actions")
		actions = func()
		func = getattr(mod, "init_outputs")
		json_outputs = func()
	except AttributeError:
		print 'function not found ' + "init_actions"
	

def get_funct(funct_name,package_name):
	try:
		func = getattr(sys.modules[package_name], funct_name)
	except AttributeError:
		print 'function not found ' + funct_name
	else:
		return func
run_proxy('openweathermap')
print filter_outputs(json.loads('{"output": {"temperature": "string","pressure":"float", "windspeed":"int"}}'),json.loads('''{
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
}'''))
'''if __name__ == "__main__":
	run_proxy('openweathermap')
	print str(actions)
	interface.run(port=8000)'''

