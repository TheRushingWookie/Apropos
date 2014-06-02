import requests
import proxy
import os
class mailgun(proxy.proxy):
    config_file_path = os.getcwd() + "/proxies/mailgun_json_config.json"
    output_tag_paths = {'message': ['message'],'id':['id']}
    input_tags = ['from','to','subject','text']
    def send_message(self, json_command):
        url = 'https://api.mailgun.net/v2/%s/messages'
        json_input = json_command['input']
        self.logger.warn('json command %s', json_command)
        if 'apikey' in json_command and 'from' in json_input:
            url = url % (json_input['from'],)
        else:
            raise Exception('Missing authentication parameter "apikey" or "from".')
        data = {"from": "<postmaster@%s>" % json_input['from'],
                  "to": json_input["to"],
                  "subject": json_input["subject"],
                  "text": json_input["text"]}
        auth = "api", "%s" % json_command['apikey']
        self.logger.debug("url: %s. \nauth: %s\ndata: %s" % (url,auth,data))
        response = requests.post(
            url,
            auth=(auth),
            data=data)
        self.logger.debug('mailgun response %s', response.json())
        return response.json()
    def init_actions(self):
        return {'sendmail':self.send_message}