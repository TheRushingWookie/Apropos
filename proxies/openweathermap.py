import json
import urllib2
import sys
import proxy
class openweathermap(proxy.proxy):
	def __init__ (self):
		self.actions = self.init_actions()
		self.json_outputs = self.init_outputs()
	def init_actions(self):
		return {'weather':[__name__,'get_weather']}
	def get_weather(self,json_input):
		
		base_url = 'http://api.openweathermap.org/data/2.5/weather?'
		if 'city' in json_input:
			base_url += 'q=' + json_input['city']
		elif 'latitude' in json_input and 'longitude' in json_input:
			base_url += 'lat=' + json_input[latitude] + '&lon=' + json_input[longitude]
		


		self.json_output = urllib2.urlopen(base_url).read()
		
		return self.json_output
	def init_outputs(self):
		return {'temperature' : self.output_temperature,
				'pressure' : self.output_pressure,
				'windspeed' : self.output_windspeed}
	def output_temperature(self,json_output):
		temp =  json_output['main']['temp']
		temp = self.convert_kelvin_to_fahrenheit(temp)
		return temp
		
	def output_pressure(self,json_output):
		temp =  json_output['main']['pressure']
		return temp
		
	def output_windspeed(self,json_output):
		temp =  json_output['wind']['speed']
		return temp
		

	#print get_weather({'city':'Bethesda, MD'})
	def convert_kelvin_to_fahrenheit(self,Kelvin_temp):
		return (Kelvin_temp - 273.15) * 1.8 + 32
