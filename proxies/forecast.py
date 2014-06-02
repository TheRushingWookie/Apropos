import requests
import proxy
import os
class forecast(proxy.proxy):
    config_file_path = os.getcwd() + "/proxies/forecast_json_config.json"
    output_tag_paths = {'temperature': ['currently', 'temperature'],'adadad':['currently', 'temperature']}
    input_tags = ['longitude','latitude']


    def get_weather(self, json_input):
        """
        Usage:
        print get_weather({'input': {'city': 'Bethesda, MD'}})
        """
        url = 'https://api.forecast.io/forecast/'
        if 'apikey' in json_input:
            url += json_input['apikey'] + '/'
        else:
            raise Exception('Missing authentication parameter "apikey".')
        # Client has longitude and latitude as input

        if 'latitude' in json_input['input'] and 'longitude' in json_input['input']:
            url += json_input['input']['latitude'] + ',' + json_input['input']['longitude']
            r = requests.get(url, headers={'User-Agent': 'Apropos'})
            self.logger.warn('url %s ' % url)
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

