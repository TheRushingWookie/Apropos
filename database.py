import sqlite3
import uuid
from time import gmtime, strftime
conn = sqlite3.connect('apis.db')
def create_apropos_tables (database_name):
	conn = sqlite3.connect(database_name + '.db')
	c = conn.cursor()

	# Create table
	c.execute('''CREATE TABLE tags ( tag_name text )''')
	c.execute('''CREATE TABLE tagmap ( tag_id integer, api_id integer)''')
	c.execute('''CREATE TABLE api_providers (date text, api_provider_name text, email text, owner_key text)''')
	c.execute('''CREATE TABLE api_endpoints (date text, api_name text, owner_key text)''')
	# Insert a row of data
	
	# Save (commit) the changes	
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
def generate_uuid ():
	return str(uuid.uuid4())
def if_provider_exists (provider_name):
	c = conn.cursor()

	provider_results = c.execute ('''Select api_provider_name from api_providers where api_provider_name = ?''', (provider_name,)).fetchall()
	if len (provider_results) > 0:
		return True
	else:
		return False
def register_api_provider (api_provider_name,email):
	c = conn.cursor()
	time = strftime("%a, %d %b %Y %X +0000", gmtime())
	if not if_provider_exists(api_provider_name):
		provider_key = generate_uuid()
		c.execute("insert into api_providers values (?, ?, ?, ?)", (time, api_provider_name, email, provider_key))
		return provider_key
	else:
		return None
print(register_api_provider("Example_provider", "example@example.com"))

def add_api_endpoint (api_provider_name, api_name,params):
	c = conn.cursor()
	provider_results = c.execute ('''Select api_name from apis where api_name = (?)''', (api_provider_name)).fetchall()
	if len (provider_results) > 0:
		return "Already Reg"
def query_api(tags):
	c = conn.cursor()
	c.execute('''SELECT b.*
					FROM tagmap tm, apis apis, tag t
					WHERE t.rowid = tm.tag_id
					AND (t.tag_name IN (?))
					AND apis.rowid = tm.api_id
					GROUP BY apis.id
					HAVING COUNT( apis.id )=(?)''' (tags), (len(tags)))
#create_apropos_tables('apis')