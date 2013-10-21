import sqlite3
import uuid
from time import gmtime, strftime
import os
dir = os.path.split(os.path.abspath(__file__))[0]
conn = sqlite3.connect(dir + '/API.db')

def create_apropos_tables (database_name):
	conn = sqlite3.connect(dir + database_name)
	# Create table
	c = conn.cursor()
	c.execute('''CREATE TABLE tags ( tag_name text )''')
	c.execute('''CREATE TABLE tagmap ( tag_id integer, api_id integer)''')
	c.execute('''CREATE TABLE api_providers (date text, api_provider_name text, email text, owner_key text)''')
	#FOREIGN KEY(api_provider_id) REFERENCES api_providers(rowid))		
	c.execute('''CREATE TABLE api_endpoints
		(date text, 
		api_name text,
		api_url text,
		owner_key text,
		category text,
		api_provider_id integer,
		FOREIGN KEY(owner_key) REFERENCES api_providers(owner_key))			
		''')
	# Insert a row of data
	
	# Save (commit) the changes	
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
#create_apropos_tables('database')
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
		conn.commit()
		return provider_key
	else:
		return None
#print(register_api_provider("Example_provider", "example@example.com"))

def add_api_endpoint (api_provider_name, api_name, api_url, owner_key, category, tags):
	c = conn.cursor()
	owner_verified  = c.execute (''' select rowid from api_providers where owner_key = (?) AND api_provider_name = (?)''', (owner_key,api_provider_name,))
	if len(owner_verified.fetchall()) > 0:
		time = strftime("%a, %d %b %Y %X +0000", gmtime())
		provider_results = c.execute ('''Select api_name from api_endpoints where api_name = (?)''', (api_name,)).fetchall()
		if len(provider_results) > 0:
			return False
		else:
			c.execute('''insert into api_endpoints values (?,?,?,?,?,?)''', (time, api_name, api_url, owner_key, category,str(provider_results)))
			api_id = c.lastrowid
			for tag in tags:
				prev_tag = c.execute('''select rowid from tags where tag_name = (?)''', (tag,)).fetchall()
				if len(prev_tag) > 0:
					tag_id = prev_tag[0][0]
					
				else:
					c.execute('''insert into tags values (?)''', (tag,))

					tag_id = c.lastrowid
					

				c.execute('''insert into tagmap values (?,?)''', (tag_id,api_id))
			conn.commit()
			return True
	else:
		return False

id_example = 'c534bb1c-4dd1-4ab1-9129-2073c14efc9a'
#add_api_endpoint("Example_provider", "test_api3" ,'http://localhost:8000/query' ,id_example ,'weather',("weather","temperature","windspeed","city","latitude","longitude","pressure"))

def query_api(category,tags ):
	c = conn.cursor()
	placeholder= '?' # For SQLite. See DBAPI paramstyle.
	placeholders= ', '.join(placeholder for unused in tags)
	print c.execute('''SELECT * FROM api_endpoints''').fetchall()
	intersect_string = '''SELECT api_endpoints.*
					FROM tagmap, api_endpoints, tags
					WHERE tags.rowid = tagmap.tag_id
					AND api_endpoints.category = (?)
					AND (tags.tag_name IN (''' + placeholders + '''))
					AND api_endpoints.rowid = tagmap.api_id
					GROUP BY api_endpoints.rowid
					HAVING COUNT( api_endpoints.rowid )=(?)'''
	query_rows = c.execute(intersect_string, (category,) + tags + (len(tags),))
	filtered_rows = []
	for row in query_rows:
		print row
		filtered_rows.append([row[2]])
	return filtered_rows
print ( " got "  + str(query_api('weather',('latitude',),)[0][0]))

#create_apropos_tables('apis')
def print_table(table_name):
	c = conn.cursor()
	print(c.execute('''SELECT * FROM (?)''', (table_name,)).fetchall())
