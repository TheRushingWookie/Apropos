import json
import urllib2
import sys
import proxy
class openweathermap(proxy.proxy):

	provider_key = 'ffdf55ee-ebb5-4fb7-86e2-3932cb6764b6'
	provider_name = 'Example_provider'
	domain_name = "http://localhost:5000/"
	api_name = 'openweathermap'
	
	output_tag_paths = {'temperature': ['main', 'temp'], 'temperature max': ['main', 'temp_max'], 'humidity': ['main', 'humidity'], 'pressure': ['main', 'pressure'], 'temperature minimum': ['main', 'temp_min'], 'cloudiness': ['clouds', 'all'], 'windspeed': ['wind', 'speed'], 'wind direction': ['wind', 'deg'],'bullshit':['main', 'temp_max']}
	input_tags = ['city','latitude','latitude']
	

	def get_weather(self,json_input):
		
		base_url = 'http://api.openweathermap.org/data/2.5/weather?'
		if 'city' in json_input['input']:
			base_url += 'q=' + json_input['input']['city']
		elif 'latitude' in json_input and 'longitude' in json_input['input']:
			base_url += 'lat=' + json_input['input']['latitude'] + '&lon=' + json_input['input']['longitude']
		self.logger.debug('base_url %s', base_url)
		req = urllib2.Request(base_url)
		req.add_unredirected_header('User-Agent', 'Apropos')
		json_output = urllib2.urlopen(req).read()	
		self.logger.debug("json output is %s", json_output)
		return json.loads(json_output)
			

	#print get_weather({'city':'Bethesda, MD'})
	def convert_kelvin_to_fahrenheit(self,Kelvin_temp):
		return (Kelvin_temp - 273.15) * 1.8 + 32
	def init_actions(self):
		return {'weather':self.get_weather}
