from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("apis.db")

@app.route("/query")
def query():
	c = conn.cursor()
	return str(c.execute("SELECT * FROM apis").fetchall())

@app.route("/register_api/<api_name>")
def register_api(api_name):
	return str(request.args)


@app.route("/drop_api/<api_name>")
def drop_api(api_name):
	return str(request.args)

if __name__ == "__main__":
	app.run()