
import json
import urllib2
import sys
import proxy
import logging
import requests
'''http://www.timeapi.org/utc/now'''

class TimeAPI(proxy.proxy):
	json_output_name_map = {"timezone": "timezone"}
	json_name_to_path_map = {"timezone": ["timezone"]}

	def get_time(self, json_input):
		r = requests.get('http://www.timeapi.org/' + json_input["input"]["timezone"] + '/now').text	
		return {"timezone": r}
	def init_actions(self):
		return {'time':self.get_time}