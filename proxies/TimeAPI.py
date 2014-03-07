
import json
import urllib2
import sys
import proxy
import logging
import os
import requests
'''http://www.timeapi.org/utc/now'''

class TimeAPI(proxy.proxy):
	config_file_path = os.getcwd() + "/proxies/time_json_config.json"
	output_tag_paths = {"timezone": ["timezone"]}
	input_tags = ['timezone']

	tags = output_tag_paths.keys() + input_tags
	def get_time(self, json_input):
		r = requests.get('http://www.timeapi.org/' + json_input["input"]["timezone"] + '/now').text	
		return {"timezone": r}
	def init_actions(self):
		print self.provider_key
		#self.logger.debug('GOT THIS SHIT %S', self.api_name)
		return {'time':self.get_time}

#TimeAPI().get_time({"input":{'timezone':'EST'}})