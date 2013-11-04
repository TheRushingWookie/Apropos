import json
import urllib2
import sys
import proxy
class openweathermap(proxy.proxy):
	json_output_name_map = {'temperature': 'temp', 'current_temperature' : 'temp', 'current temperature' : 'temp','max_temp' : 'temp_max','min_temp' : 'temp_min','humidity' : 'humidity', 'pressure':'pressure', 'speed' : 'speed', 'wind_direction' : 'deg', 'cloudiness' : 'cloudiness'}
							
	json_name_to_path_map = {'temp': ['main', 'temp'], 'temp_max': ['main', 'temp_max'], 'humidity': ['main', 'humidity'], 'pressure': ['main', 'pressure'], 'temp_min': ['main', 'temp_min'], 'cloudiness': ['clouds', 'all'], 'speed': ['wind', 'speed'], 'deg': ['wind', 'deg']}
	def __init__ (self):
		self.actions = self.init_actions()
		self.json_outputs = self.init_outputs()
	
	def get_weather(self,json_input):
		
		base_url = 'http://api.openweathermap.org/data/2.5/weather?'
		if 'city' in json_input['input']:
			base_url += 'q=' + json_input['input']['city']
		elif 'latitude' in json_input and 'longitude' in json_input['input']:
			base_url += 'lat=' + json_input['input'][latitude] + '&lon=' + json_input['input'][longitude]
		
		req = urllib2.Request(base_url)
		req.add_unredirected_header('User-Agent', 'Custom User-Agent')
		json_output = urllib2.urlopen(req).read()
		
		return json_output
			

	#print get_weather({'city':'Bethesda, MD'})
	def convert_kelvin_to_fahrenheit(self,Kelvin_temp):
		return (Kelvin_temp - 273.15) * 1.8 + 32
	def init_actions(self):
		return {'weather':self.get_weather}
