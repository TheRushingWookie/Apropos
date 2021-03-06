from flask import Flask, request, send_from_directory
from collections import OrderedDict
from main import *
import database
import sys
import json

from flask_cors import *

interface = Flask(__name__)


def check_assertions(request, path):
    assert sys.getsizeof(request.json) < 1048576
    assert request.path == path
    assert request.method == 'POST'


@app.route("/test")
def test_html():
    logger.debug("test page")
    return send_from_directory('/Users/quinnjarrell/Desktop/Apropos/client_lib', 'htmltestpage.html')


@app.route("/query", methods=["POST"])
@cross_origin(origins='*',headers=['Origin', 'X-Requested-With', 'Content-Type', 'Accept'])
def web_query():
    check_assertions(request, '/query')
    logger.debug("raw json input %s", request.json)
    tags = tuple(str(tag) for tag in
                 request.json["input"].keys() +
                 request.json["output"].keys())

    logger.debug("tags %s", tags)
    fuzzed_tag_map = database.find_closest_tags(tags)
    logger.debug("Fuzzed tag map %s", fuzzed_tag_map)
    fuzzed_tags = [fuzzed_tag_map[key] for key in fuzzed_tag_map.keys()]
    logger.debug("Fuzzed tags %s", fuzzed_tags)
    for tag in fuzzed_tag_map.keys():
        fuzzed_tag_map[fuzzed_tag_map[tag]] = tag
    apis = database.query_api(request.json["action"], tuple(fuzzed_tags))
    json_output = {'apis': apis,
                   'corrected_tags': fuzzed_tag_map}
    logger.debug('apis %s', apis)
    logger.debug('json_output %s', json_output)
    if json_output:
        return json.dumps(json_output)
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

    check_assertions(request, '/register_api_provider')

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


@app.route("/jsclient.js", methods=['GET'])
def js_web_client():
    return send_from_directory('/Users/quinnjarrell/Desktop/Apropos/client_lib', 'javascript_client.js')


@app.route("/register_api", methods=["POST"])
def web_register_api():
    check_assertions(request, '/register_api')
    logger.debug('raw data %s', request.data)
    if database.add_api_endpoint(request.json['api_provider'],
                                 request.json['api_name'],
                                 request.json['api_url'],

                                 request.json['category'],
                                 list(map(str, request.json['tags'])),
                                 request.json['api_login_info'],
                                 json.loads(request.data, object_pairs_hook=OrderedDict)):
        return json.dumps({"Status": True})
    else:
        return json.dumps({"Status": False})


@app.route("/update_tags", methods=["POST"])
def web_update_tags():
    logger.debug('Got json %s', request.json)
    check_assertions(request, '/update_tags')
    tags = request.json['tags']

    database.update_tags(
        request.json['api_provider'],
        request.json['api_name'],
        tags,
        json.loads(request.data)
    )
    return 'success'


@app.route("/drop_api", methods=["POST"])
def web_drop_api():
    check_assertions(request, '/drop_api')
    try:
        return "Delete " + request.json['api_name'] + " from the database"
    except:
        return json.dumps({"Status": False})


@app.route("/commit")
def commit():
    database.conn.commit()


if __name__ == "__main__":
    app.run(debug=True)
