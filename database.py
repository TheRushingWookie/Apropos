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
	#FOREIGN KEY(api_provider_id) REFERENCES api_providers(rowid))		
	c.execute('''CREATE TABLE api_endpoints 
		(date text, 
		api_name text,
		api_url text,
		owner_key text,
		api_provider_id integer,
		FOREIGN KEY(owner_key) REFERENCES api_providers(owner_key))			
		''')
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

def add_api_endpoint ( api_name, api_url, owner_key,tags):
	c = conn.cursor()
		time = strftime("%a, %d %b %Y %X +0000", gmtime())
		provider_results = c.execute ('''Select api_name from api_endpoints where api_name = (?)''', (api_name,)).fetchall()
		if len(provider_results) > 0:
			return False
		else:
			c.execute('''insert into api_endpoints values (?,?,?,?)''', (time, api_name, owner_key,0))
			api_id = c.
			for tag in tags:
				prev_tag = c.execute('''select rowid from tags where tag_name = (?)''', (tag,)).fetchall()
				if len(prev_tag) > 0:
					tag_id = prev_tag[0][0]
					
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
	query_rows = c.execute(intersect_string, tags + (len(tags),))
	filtered_rows = []
	for row in query_rows:
		filtered_rows.append([row[1]])
	return filtered_rows


#create_apropos_tables('apis')
def print_table(table_name):
	c = conn.cursor()
	print(c.execute('''SELECT * FROM (?)''', (table_name,)).fetchall())
