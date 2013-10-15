import json
import urllib2
def init_actions():
	return {'weather':[__name__,'get_weather']}
def get_weather(json_input):
	
	base_url = 'http://api.openweathermap.org/data/2.5/weather?'
	if 'city' in json_input:
		base_url += 'q=' + json_input['city']
	elif 'latitude' in json_input and 'longitude' in json_input:
		base_url += 'lat=' + json_input[latitude] + '&lon=' + json_input[longitude]
	


	json_output = urllib2.urlopen(base_url).read()
	
	return json_output
def init_outputs():
	return {'temperature' : output_temperature,
			'pressure' : output_pressure,
			'windspeed' : output_windspeed}
def output_temperature(json_output,val_type):
	temp =  json_output['main']['temp']
	temp = convert_kelvin_to_fahrenheit(temp)
	print val_type
	if val_type == 'int':
		return int(temp)
	elif val_type == 'string':
		return str(temp)
	elif val_type == 'float':
		return float(temp)
def output_pressure(json_output,val_type):
	temp =  json_output['main']['pressure']
	temp = convert_kelvin_to_fahrenheit(temp)
	print val_type
	if val_type == 'int':
		return int(temp)
	elif val_type == 'string':
		return str(temp)
	elif val_type == 'float':
		return float(temp)
def output_windspeed(json_output,val_type):
	temp =  json_output['wind']['speed']
	temp = convert_kelvin_to_fahrenheit(temp)
	print val_type
	if val_type == 'int':
		return int(temp)
	elif val_type == 'string':
		return str(temp)
	elif val_type == 'float':
		return float(temp)

#print get_weather({'city':'Bethesda, MD'})
def convert_kelvin_to_fahrenheit(Kelvin_temp):
	return (Kelvin_temp - 273.15) * 1.8 + 32