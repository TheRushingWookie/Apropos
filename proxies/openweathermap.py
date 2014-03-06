import json
import requests
import proxy

class openweathermap(proxy.proxy):

    json_name_to_path_map = {'temperature': ['main', 'temp'], 'temperature max': ['main', 'temp_max'], 'humidity': ['main', 'humidity'], 'pressure': ['main', 'pressure'], 'temperature minimum': ['main', 'temp_min'], 'cloudiness': ['clouds', 'all'], 'windspeed': ['wind', 'speed'], 'wind direction': ['wind', 'deg']}


	def get_weather(self, json_input):
	        """
	        Usage:
	        print get_weather({'input': {'city': 'Bethesda, MD'}})
	        """

	        url = 'http://api.openweathermap.org/data/2.5/weather?'

	        # Client has city as input
	        if 'city' in json_input['input']:
	            payload = {'q': json_input['input']['city']}

	        # Client has longitude and latitude as input
	        elif 'latitude' in json_input and 'longitude' in json_input['input']:
	            payload = {'lat': json_input['input']['latitude'],
	                       'lon': json_input['input']['longitude']}

	        if payload:
	            r = requests.get(url, params=payload, headers={'User-Agent': 'Apropos'})
	            if r.status_code == 200:
	                return r.json()
	            else:
	                raise Exception('Status code: {0}'.format(r.status_code))
	        else:
	            raise Exception('Invalid tags')
			


    def convert_kelvin_to_fahrenheit(self, Kelvin_temp):
        return (Kelvin_temp - 273.15) * 1.8 + 32


    def init_actions(self):
        return {'weather':self.get_weather}
