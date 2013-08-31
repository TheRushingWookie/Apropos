from flask import Flask
from flask import g
import sqlite3

db = "apis.db"

def get_db():
	dbobj = getattr(g, "_database", None)
	if dbobj is None:
		dbobj = g._database = sqlite3.connect("apis.db")
	return dbobj

def close_connection(exception):
    dbobj = getattr(g, '_database', None)
    if dbobj is not None:
        dbobj.close()

app = Flask(__name__)

@app.route("/query")
def query():
	cur = get_db().cursor()
	return cur.execute("SELECT * FROM apis").fetchall()

@app.route("/register_api/<api_name>")
def register_api(api_name):
	return str("Register page " + str(api_name))

@app.route("/drop_api/<api_name>")
def drop_api(api_name):
	return str("API dropped " + str(api_name))

if __name__ == "__main__":
	app.run()
