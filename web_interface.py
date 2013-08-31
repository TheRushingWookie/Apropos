from flask import Flask
from flask import request
import sqlite3

# Create flask object
interface = Flask(__name__)

# Open an sqlite connection
conn = sqlite3.connect("apis.db")

# apropros.com/query
@interface.route("/query")
def query():
	try:
		c = conn.cursor()
		# Print out the entire database
		return str(c.execute("SELECT * FROM apis").fetchall())
	except:
		return "Something went wrong..."

# apropros.com/register_api/api_name&tag=...
@interface.route("/register_api/<api_name>")
def register_api(api_name):
	try:
		# Returns all values with "tag" as the key
		return str(dict(request.args)["tag"])
	except:
		return "Something went wrong..."

# apropros.com/drop_api/api_name
@interface.route("/drop_api/<api_name>")
def drop_api(api_name):
	try:
		# sqlite implementation to be implemented
		return "Delete " + api_name + " from the database"
	except:
		return "Something went wrong..."

# Run only if called in this script
if __name__ == "__main__":
	interface.run()
