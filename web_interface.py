from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/query")
def query():
	conn = sqlite3.connect("apis.db")
	c = conn.cursor()
	
	return "Query page"

@app.route("/register_api/<api_name>")
def register_api(api_name):
	return str("Register page " + str(api_name))

@app.route("/drop_api/<api_name>")
def drop_api(api_name):
	return str("API dropped " + str(api_name))

if __name__ == "__main__":
	app.run()
