#!/usr/bin/python

from flask import Flask
from flask import request
import json
import urllib2
import smtplib
import pdb
import unicodedata
import database


def send_email(user, password, user_address, receiver, message):

    # Initialize SMTP server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, password)

    # Send email
    server.sendmail(user_address, receiver, message)
    server.quit()
# Create flask object
interface = Flask(__name__)
# def uumd_to_list(umd, key):
# converts unicode UnmutableMultiDict to a list
# 	unicode_list = list(dict(uumd)[key])
# 	list = []
# 	for item in list:
# 		list.append(str(item))
# 	return list


# apropros.com/query?action=...&input=...&output=
# example: localhost:5000/query?action=weather&input=weather&output=temperature
@interface.route("/query")
def web_query():
    immutable_multi_dict = request.args
    norm_dict = dict(immutable_multi_dict)
    print norm_dict
    action = norm_dict["action"][0]
    tags = tuple(str(_) for _ in norm_dict["input"] + norm_dict["output"])
    print tags

    apis = {'apis': database.query_api(action, tuple(tags))}
    print "apis is " + str(apis)
    if apis:
        return urllib2.quote(json.dumps(apis))
    else:
        return json.dumps({"Status": False})

# apropros.com/register_api_provider?api_provider=...&contact_info=...
@interface.route("/register_api_provider")
def web_register_api_provider():
    """
    To-do:
            - check if valid email
            - check if no other html parameters entered
            - add rate limiter
    """
    try:
        api_provider = str(dict(request.args)["api_provider"][0])
        contact_info_string = str(dict(request.args)["contact_info"][0])
        registration_key = database.register_api_provider(
            api_provider, contact_info_string)
        print registration_key
        if registration_key:
            send_email("13917714j", "3019236Q", "13917714j@gmail.com",
                       contact_info_string, registration_key)
            return json.dumps({"Status1": True})
        else:
            return json.dumps({"Status2": False})
    except:
        return json.dumps({"Status3": False})

# apropros.com/register_api?api_provider=...&api_name=...&api_url=...&provider_key=...&action=...&tag=...
@interface.route("/register_api")
def web_register_api():
    try:
        param_dict = dict(request.args)

        api_provider = param_dict['api_provider'][0]
        api_name = param_dict['api_name'][0]
        api_url = param_dict['api_url'][0]
        api_action = param_dict['action'][0]
        provider_key = param_dict['provider_key'][0]

        tags_unicode = json.loads(param_dict['tags'][0])
        tags = []

        for tag in tags_unicode:
            tags.append(str(tag))
        print api_provider, api_name, api_url, provider_key, tags
        if database.add_api_endpoint(api_provider, api_name, api_url, provider_key, api_action,  tags):
            return json.dumps({"Status": True})
        else:
            return json.dumps({"Status1": False})
    except:
        return json.dumps({"Status2": False})

# apropros.com/drop_api?api_name=...
@interface.route("/drop_api")
def web_drop_api():
    try:
        api_name = str(list(dict(request.args)["api_name"])[0])
        return "Delete " + api_name + " from the database"
    except:
        return json.dumps({"Status": False})


@interface.route("/commit")
def commit():
    database.conn.commit()

if __name__ == "__main__":
    interface.run()
