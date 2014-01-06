#!/usr/bin/python

from flask import Flask
from flask import request
from main import *
import ast
import sys
import json
import urllib2
import smtplib
import pdb
import unicodedata

interface = Flask(__name__)

def send_email(user, password, user_address, receiver, message):
    # Initialize SMTP server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, password)

    # Send email
    server.sendmail(user_address, receiver, message)
    server.quit()

# apropros.com/query?action=...&input=...&output=
# example: localhost:5000/query?action=weather&input=weather&output=temperature
@app.route("/query", methods=["POST"])
def web_query():
    if request.method == "POST":
        if len(str(request.form)) < sys.maxint / 1000000000000:
            data = ast.literal_eval(json.dumps(request.form))
            data["input"] = ast.literal_eval(data["input"])
            data["output"] = ast.literal_eval(data["output"])
            action = data["action"]
            print action

            tags = tuple(str(_) for _ in data["input"].keys() + data["output"].keys())
            print tags

            apis = {'apis': database.query_api(action, tuple(tags))}
            print apis
            if apis:
                return urllib2.quote(json.dumps(apis))
            else:
                return json.dumps({"Status": False})
        else:
            return json.dumps({"Status": False})

# apropros.com/register_api_provider?api_provider=...&contact_info=...
@app.route("/register_api_provider")
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


@app.route("/register_api")
def web_register_api():
    try:
        param_dict = dict(request.args)

        api_provider = param_dict['api_provider'][0]
        api_name = param_dict['api_name'][0]

        api_url = param_dict['api_url'][0]
        
        api_category = param_dict['category'][0]

        provider_key = param_dict['provider_key'][0]
        api_login_info = param_dict['api_login_info'][0]
        tags_unicode = param_dict['tags'][0]
        tags = []

        for tag in tags_unicode:
            tags.append(str(tag))
        print api_provider, api_name, api_url, provider_key, tags
        if database.add_api_endpoint(api_provider, api_name, api_url, provider_key, api_category, tags, api_login_info):
            return json.dumps({"Status": True})
        else:
            return json.dumps({"Status1": False})
    except Exception as e:
        app.logger.warning('Failed with %s', e)
        return json.dumps({"Status2": False})

# apropros.com/drop_api?api_name=...
@app.route("/drop_api")
def web_drop_api():
    try:
        api_name = str(list(dict(request.args)["api_name"])[0])
        return "Delete " + api_name + " from the database"
    except:
        return json.dumps({"Status": False})


@app.route("/commit")
def commit():
    database.conn.commit()

if __name__ == "__main__":
    app.run(debug=True)

