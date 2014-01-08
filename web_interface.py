#!/usr/bin/python

from flask import Flask, request, jsonify
from main import *
import database
import sys
import json

interface = Flask(__name__)


@app.route("/query", methods=["POST"])
def web_query():
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == '/query'
    assert request.method == 'POST'

    tags = tuple(str(tag) for tag in
                 request.json["input"].keys() +
                 request.json["output"].keys())
    apis = {'apis': database.query_api(request.json["action"], tuple(tags))}

    if apis:
        return json.dumps(apis)
    else:
        return json.dumps({"Status": False})


@app.route("/register_api_provider", methods=["POST"])
def web_register_api_provider():
    """
    To-do:
        - check if valid email
        - check if no other html parameters entered
        - add rate limiter
    """
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == '/register_api_provider'
    assert request.method == 'POST'

    def send_email(username, password, user_address, receiver, message):
        import smtplib

        # Initialize SMTP server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)

        # Send email
        server.sendmail(user_address, receiver, message)
        server.quit()

    api_provider = request.json["api_provider"]
    contact_info = request.json["contact_info"]

    registration_key = database.register_api_provider(api_provider,
                                                      contact_info)

    if registration_key:
        send_email("13917714j",
                   "3019236Q",
                   "13917714j@gmail.com",
                   contact_info,
                   registration_key)

        return json.dumps({"Status": True})
    else:
        return json.dumps({"Status": False})


@app.route("/register_api", methods=["POST"])
def web_register_api():
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == '/register_api'
    assert request.method == 'POST'

    tags_unicode = request.json['tags']
    tags = []

    for tag in tags_unicode:
        tags.append(str(tag))

    if database.add_api_endpoint(request.json['api_provider'],
                                 request.json['api_name'],
                                 request.json['api_url'],
                                 request.json['provider_key'],
                                 request.json['category'],
                                 map(str, request.json['tags']),
                                 request.json['api_login_info']):
        return json.dumps({"Status": True})
    else:
        return json.dumps({"Status": False})


@app.route("/drop_api", methods=["POST"])
def web_drop_api():
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == '/drop_api'
    assert request.method == 'POST'

    try:
        return "Delete " + request.json['api_name'] + " from the database"
    except:
        return json.dumps({"Status": False})


@app.route("/commit")
def commit():
    database.conn.commit()

if __name__ == "__main__":
    app.run(debug=True)
