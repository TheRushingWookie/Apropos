import sqlite3
import uuid
from time import gmtime, strftime
conn = sqlite3.connect('apis.db')
def create_apropos_tables (database_name):
	c = conn.cursor()
	# Create table
	c.execute('''CREATE TABLE tags ( tag_name text )''')
	c.execute('''CREATE TABLE tagmap ( tag_id integer, api_id integer)''')
	c.execute('''CREATE TABLE api_providers (date text, api_provider_name text, email text, owner_key text)''')
	c.execute('''CREATE TABLE api_endpoints 
		(date text, 
		api_name text,
		owner_key text,
		FOREIGN KEY(owner_key) REFERENCES api_providers(owner_key))''')
	# Insert a row of data
	
	# Save (commit) the changes	
	conn.commit()
	conn.close()
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
#print(register_api_provider("Example_provider", "example@example.com"))

def add_api_endpoint (api_provider_name, api_name, owner_key,tags):
	c = conn.cursor()
	owner_verified  = c.execute (''' select owner_key,api_provider_name from api_providers where owner_key = (?) AND api_provider_name = (?)''', (owner_key,api_provider_name,))
	if len(owner_verified.fetchall()) > 0:
		time = strftime("%a, %d %b %Y %X +0000", gmtime())
		provider_results = c.execute ('''Select api_name from api_endpoints where api_name = (?)''', (api_name,)).fetchall()
		if len(provider_results) > 0:
			return "API " + api_name + " already exists" 
		else:
			c.execute('''insert into api_endpoints values (?,?,?)''', (time, api_name, owner_key,))
			api_id = c.lastrowid
			for tag in tags:
				prev_tag = c.execute('''select tag_name from tags where tag_name = (?)''', (tag,))
				if len(prev_tag.fetchall()) > 0:
					tag_id = prev_tag.fetchone()
				else:
					c.execute('''insert into tags values (?)''', (tag,))
					tag_id = c.lastrowid
				c.execute('''insert into tagmap values (?,?)''', (tag_id,api_id))
			return "Added API"
	else:
		return "User not verified"
			

def query_api(tags):
	c = conn.cursor()
	return c.execute('''SELECT t.*
					FROM tagmap tm, apis apis, tag t
					WHERE t.rowid = tm.tag_id
					AND (t.tag_name IN (?))
					AND apis.rowid = tm.api_id
					GROUP BY apis.id
					HAVING COUNT( apis.id )=(?)''' (tags), (len(tags))).fetchall()
#create_apropos_tables('apis')
