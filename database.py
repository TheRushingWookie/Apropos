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
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
def generate_uuid ():
	return str(uuid.uuid4())
def if_provider_exists (provider_name,c):
	provider_results = c.execute ('''Select api_provider_name from api_providers where api_provider_name = ?''', (provider_name,)).fetchall()
	if len (provider_results) > 0:
		return True
	else:
		return False
def register_api_provider (api_provider_name,email):
	c = conn.cursor()
	time = strftime("%a, %d %b %Y %X +0000", gmtime())
	if not if_provider_exists(api_provider_name,c):
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
			return False
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
			return True
	else:
		return False
'''
id_example = register_api_provider("Example_provider", "example@example.com")
add_api_endpoint("Example_provider", "test_api" , id_example ,("weather","temperature","windspeed"))'''			

def query_api(tags):
	c = conn.cursor()
	placeholder= '?' # For SQLite. See DBAPI paramstyle.
	placeholders= ', '.join(placeholder for unused in tags)
	intersect_string = '''SELECT api_endpoints.*
					FROM tagmap, api_endpoints, tags
					WHERE tags.rowid = tagmap.tag_id
					AND (tags.tag_name IN (''' + placeholders + '''))
					AND api_endpoints.rowid = tagmap.api_id
					GROUP BY api_endpoints.rowid
					HAVING COUNT( api_endpoints.rowid )=(?)'''
	return c.execute(intersect_string, tags + (len(tags),)).fetchall()
#create_apropos_tables('apis')
def print_table(table_name):
	c = conn.cursor()
	print(c.execute('''SELECT * FROM (?)''', (table_name,)).fetchall())
