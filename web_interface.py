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
		return str(c.execute("SELECT * FROM apis").fetchall())
	except:
		return

# apropros.com/register_api/...
@interface.route("/register_api/<api_name>")
def register_api(api_name):
	try:
		return str(request.args)
	except:
		return

# apropros.com/drop_api/...
@interface.route("/drop_api/<api_name>")
def drop_api(api_name):
	try:
		return str(request.args)
	except:
		return

# Run only if called in this script
if __name__ == "__main__":
	interface.run()
