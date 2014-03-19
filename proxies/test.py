import json, requests

def get_weather(json_input):
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    # Client has city as input
    if 'city' in json_input['input']:
        payload = {'q': json_input['input']['city']}
    # Client has longitude and latitude as input
    elif 'latitude' in json_input and 'longitude' in json_input['input']:
        payload = {'lat': json_input['input']['latitude'],
                   'lon=': json_input['input']['longitude']}
    if payload:
        r = requests.get(url, params=payload, headers={'User-Agent': 'Apropos'})
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Status code: {0}'.format(r.status_code))
    else:
        raise Exception('Invalid tags')

print get_weather({'input':{'city':'Bethesda,MD'}})
