import json
import urllib2
def init_actions():
	return {'weather':[__name__,'get_weather']}
def get_weather(json):
	print('getweather')
	base_url = 'http://api.openweathermap.org/data/2.5/weather?'
	if 'city' in json:
		base_url += 'q=' + json['city']
	elif 'latitude' in json and 'longitude' in json:
		base_url += 'lat=' + json[latitude] + '&lon=' + json[longitude]
	


	json = urllib2.urlopen(base_url)
	
	return str(json.read())
#get_weather({'city':'Bethesda, MD'})