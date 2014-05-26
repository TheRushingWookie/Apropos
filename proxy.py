import json
import os
import traceback
import sys
import requests
import hmac
import base64
from os.path import *
from flask import Flask, make_response, request
from collections import OrderedDict
from hashlib import sha1
from flask_cors import *
import logging
from logging import FileHandler
class RoutingData(object):

    def __init__(self, args, kwargs):
        super(RoutingData, self).__init__()
        self.args = args
        self.kwargs = kwargs


def route(*args, **kwargs):
    def wrap(fn):
        l = getattr(fn, '_routing_data', [])
        l.append(RoutingData(args, kwargs))
        fn._routing_data = l
        return fn
    return wrap


class SuperFlask(Flask):

    def __init__(self, import_name):
        super(SuperFlask, self).__init__(import_name)
        self.endpoint_prefix = None
        for name in dir(self):
            if hasattr(getattr(self, name), ("_routing_data")):
                fn = getattr(self, name)
                rds = fn._routing_data
                for rd in rds:
                    self.route(*rd.args, **rd.kwargs)(fn)

class proxy(SuperFlask):
    output_tag_paths = []
    provider_key = ''
    provider_name = ''
    domain_name = "http://localhost:5000/"
    api_name = ''
    tags = []
    port = None
    input_tags = []
    config_file_path = os.getcwd() + "/json_config.json"
    # update_tags(api_provider_name,api_endpoint_name,owner_key,new_tags)

    @route("/query", methods=['POST', 'OPTIONS'])
    @cross_origin(origins='*',headers=['Origin', 'X-Requested-With', 'Content-Type', 'Accept'])
    def query(self):
        io_json_dict = request.json
        # return str(instance.actions)
        #io_json_dict = json.loads(io_json_dict)
        #self.logger.debug('Json is %s', io_json_dict)
        action = io_json_dict['action']
        if action:
            print(str(action))
            funct = self.actions[str(action)]
            self.logger.warn("request.json %s" % (request.json))
            self.logger.debug("Funct selected is %s", str(funct))
            json_output = funct(io_json_dict)
            self.logger.debug("json_output %s", str(json_output))
            callback = request.args.get('callback')
            if callback:
                return '{0}({1})'.format(callback, self.filter_outputs(io_json_dict, json_output))
            else:
                return self.filter_outputs(io_json_dict, json_output)
        return "No action"

    def load_config(self):
        '''Loads a json config file to provide initialization values for provider_key, provider_name, domain_name, api_name.'''
        with open(self.config_file_path, 'r') as json_file:
            json_string = json_file.read()
            print json_string
            json_config = json.loads(json_string)
            self.provider_key = json_config['provider_key']
            self.provider_name = json_config['provider_name']
            self.domain_name = json_config['domain_name']
            self.api_name = json_config['api_name']
            self.port = json_config['port']

    def write_config(self):
        '''Writes a json config file which includes provider_key, provider_name, domain_name, api_name.'''
        with open(self.config_file_path, 'w') as json_file:
            json_data = {
                'port': self.port, 'provider_name': self.provider_name,
                'domain_name': self.domain_name, 'api_name': self.api_name}
            json_file.write(json.dumps(json_data, json_file, indent=4))
            json.dumps(json_data, json_file)

    def __init__(self, import_name):
        super(proxy, self).__init__(import_name)
        a = logging.getLogger(name='proxies.forecast')
        file_handler = FileHandler('/Users/quinnjarrell/Desktop/Apropos/' + self.logger_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        a.addHandler(file_handler)
        self.tags = self.output_tag_paths.keys() + self.input_tags
        self.actions = self.init_actions()
        self.json_outputs = self.init_outputs()
        self.logger.warn('works %s' % self.logger)


    def standard_type_converter(self, val, val_type):
        '''Converts all standard types such as integer, string'''
        val_type = val_type.lower()
        self.logger.debug("val_type " + val_type + ' ' + str(val))
        try:
            if val_type == 'int' or val_type == 'integer':
                if val.find('.'):
                    return int(float(val))
                return int(val)
            elif val_type == 'string':
                return str(val)
            elif val_type == 'float':
                return float(val)
        except:
            #  Might want to make str(val) keep escaped characters
            print "Bad conversion of " + str(val) + " + with type " + str(val_type)
        return val

    def custom_type_converter(self, val, val_type):
            '''Stub function to let conversions of individuation'''
            return val

    def filter_outputs(self, json_input, output):
        '''Filters the output of an api into what is requested and makes sure the data conforms to SI Units'''
        filtered_json = {}
        for i in json_input['output'].keys():

            try:
                funct = self.json_outputs[i]

                self.logger.debug(self.json_outputs)
                converted_val = funct(output, i)
                # print "Filterd " + converted_val
                filtered_json[i] = self.standard_type_converter(
                    converted_val, json_input['output'][i])
                # print "Filterd " + str(type(filtered_json[i]))
                filtered_json[i] = self.custom_type_converter(
                    filtered_json[i], json_input['output'][i])
                # print "Filterd 2 " + str(type(filtered_json[i]))
                # print str(type(converted_val))
            except Exception, e:
                self.logger.debug(str(e))
                return str(traceback.format_exc())
                return json.dumps({'wrong_outputs': i})
        return json.dumps(filtered_json)

    def get_key_hmac(self, base_string):
        assert (self.provider_key)
        return base64.urlsafe_b64encode(hmac.new(self.provider_key.encode('ascii'), base_string.encode('ascii'), sha1).digest())

    def hmac_json_string(self, json_input_unordered):
        json_input = OrderedDict(
            sorted(json_input_unordered.items(), key=lambda t: t[0]))
        hmac = self.get_key_hmac(json.dumps(json_input))
        json_input['hmac'] = hmac
        return json.dumps(json_input)

    def update_tags(self, tags):
        payload = {'api_provider': self.provider_name,
                   'api_name': self.api_name, 'tags': self.tags}
        print self.tags
        payload_string = self.hmac_json_string(payload)
        headers = {'content-type': 'application/json'}
        r = requests.post(
            self.domain_name + 'update_tags', data=payload_string, headers=headers)

    def query_access_funct(self, json_output, field):
        path = self.output_tag_paths[field]
        self.logger.debug("path %s", path)
        self.logger.debug("field %s", field)
        self.logger.debug('json_output %s', json_output)
        if json_output != None:
            for i in path:
                if i in json_output:
                    json_output = json_output[i]
                else:
                    self.logger.debug(
                        'Path to %s is messed up. %s ', i, json_output)
                    return "Path to json field is messed up"
            return json_output
        else:
            return "Null"

    def init_outputs(self):
        self.load_config()
        self.update_tags(self.tags)
        field_names = self.output_tag_paths
        field_funct_hash = {}
        name_conversions = {}
        for key in field_names.keys():
            field_funct_hash[key] = self.query_access_funct

        return field_funct_hash

    def init_actions(self):

        return None

    def get_funct(self, funct_name, package_name):
        try:
            func = getattr(sys.modules[package_name], funct_name)
        except AttributeError:
            print 'function not found ' + funct_name
        else:
            return func
