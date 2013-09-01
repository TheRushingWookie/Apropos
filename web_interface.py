#!/usr/bin/python

from flask import Flask
from flask import request
import sqlite3
import json

# Create flask object
interface = Flask(__name__)

# Open an sqlite connection
conn = sqlite3.connect("apis.db")

# apropros.com/query
@interface.route("/query")
def web_query():
	try:
		tags = dict(request.args)["tag"]
		database = str(c.execute("SELECT * FROM apis").fetchall())
		c = conn.cursor()
		
	except:
		return "Something went wrong..."

@interface.route("/register_api_provider/<api_provider>")
def web_register_api_provider(api_provider):
	# to-do: check if provider already exists
	try:

		return str(str(api_provider) + str(dict(request.args)["contact_info"]))
	except:
		return "Something went wrong..."

# apropros.com/register_api/api_name&tag=...
@interface.route("/register_api/<api_name>")
def web_register_api(api_name):
	try:
		# Returns all values that have "tag" as the key
		return str(str(api_name) + str(dict(request.args)["tag"]))
	except:
		return "Something went wrong..."

# apropros.com/drop_api/api_name
@interface.route("/drop_api/<api_name>")
def web_drop_api(api_name):
	try:
		# sqlite implementation to be implemented
		return "Delete " + api_name + " from the database"
	except:
		return "Something went wrong..."

if __name__ == "__main__":
	interface.run()
