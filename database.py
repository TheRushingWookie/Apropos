import sqlite3
import uuid
from time import gmtime, strftime
import os
from fuzzywuzzy import process,fuzz
conn = sqlite3.connect(os.getcwd() + '/API.db',check_same_thread=False)

def create_apropos_tables (database_name):
	#conn = sqlite3.connect(dir + database_name)
	# Create table
	c = conn.cursor()
	c.execute('''CREATE TABLE tags ( tag_name text )''')
	c.execute('''CREATE TABLE tagmap ( tag_id integer, api_id integer)''')
	
	
	c.execute('''CREATE TABLE api_providers (date text, api_provider_name text, email text, owner_key text)''')
	
	c.execute('''CREATE TABLE api_endpoints
		(date text, 
		api_name text,
		api_url text,
		owner_key text,
		category text,
		api_provider_id integer,
		FOREIGN KEY(owner_key) REFERENCES api_providers(owner_key))			
		''')
	c.execute('''CREATE TABLE api_keys (date text,  key_name text , api_endpoint_id integer, FOREIGN KEY(api_endpoint_id) REFERENCES api_endpoints(rowid))''')
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
def add_api_key (api_provider_name, api_endpoint_name, owner_key, key_name):
	c = conn.cursor()
	owner_verified  = c.execute (''' select rowid from api_providers where owner_key = (?) AND api_provider_name = (?)''', (owner_key,api_provider_name,))
	if len(owner_verified.fetchall()) > 0:
		endpoint = c.execute (''' select rowid from api_endpoints where api_name = (?) AND owner_key = (?)''', (api_endpoint_name,owner_key)).fetchall()[0][0]
		time = strftime("%a, %d %b %Y %X +0000", gmtime())
		#print "key is "  + str(endpoint)
		provider_results = c.execute ('''Select key_name, api_endpoint_id from api_keys where key_name = (?) and api_endpoint_id = (?)''', (key_name, endpoint)).fetchall()
		if len(provider_results) > 0:
			return False
		else:

			c.execute('''insert into api_keys values (?,?,?)''', (time, key_name, endpoint))

def print_table(table_name):
	c = conn.cursor()
	results = c.execute('''select * from ''' + table_name ).fetchall()
	print results

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
test_api_id = ""
def create_test_db ():
	global test_api_id
	create_apropos_tables('apis')
	test_api_id = register_api_provider("Example_provider", "example@example.com")
	#print print_table("api_endpoints")
	add_api_endpoint("Example_provider", "test_api3" ,'http://localhost:7000/query' ,test_api_id ,'weather',('city','latitude','longitude','lat','lng','long','humidity', 'pressure', 'cloudiness', 'temperature', 'min_temp', 'current temperature', 'max_temp', 'speed', 'wind_direction'))
	add_api_endpoint("Example_provider", "YahooStocks" ,'http://localhost:8000/query' ,test_api_id ,'stocks',('stock_symbol','Two Hundred day Moving Average', 'Days High', 'Price To Sales Ratio', 'Last Trade Date', 'Book Value', 'Percent Change From Year High', 'Previous Close Price', 'asking price', 'Fifty day Moving Average', 'Days Low', 'Symbol', 'Change From Year High', 'Stock Name', 'Year High', 'Stock Exchange', 'Price Earning Growth Ratio', 'EBITDA', 'Change From Fifty day Moving Average', 'Average Daily Volume', 'Percent Change From Fifty day Moving Average', 'Last Trade Time', 'Year Low', 'Bid', 'Price To Book Ratio', 'Percent Change From Two Hundred day Moving Average', 'Open Price', 'Volume', 'Percent Change From Year Low', 'Short Ratio', 'Change From Year Low', 'Price Earnings Ratio', 'Change From Two Hundred day Moving Average', 'Year Range', 'Market Capitalization'))
	add_api_endpoint("Example_provider", "WebServiceXStocks" ,'http://localhost:9000/query' ,test_api_id ,'stocks',('stock_symbol', 'Days High', 'Last Trade Date', 'Price Earnings Ratio', 'Year Range', 'P-E', 'Low', 'Open Price', 'MktCap', 'Earns', 'Last Trade Time', 'Symbol', 'Previous Close Price', 'Change in percent', 'Volume', 'PreviousClose', 'Days Low', 'Date', 'Change', 'Stock Name', 'Time', 'PercentageChange', 'High', 'Market Capitalization', 'Change in Realtime', 'AnnRange', 'Last Trade Price', 'Open', 'Earnings per Share'))
	add_api_key("Example_provider","test_api3",test_api_id,"1239123")
	add_api_key("Example_provider","test_api3",test_api_id,"wdwd")
	conn.commit()
	print_table('api_endpoints')
#create_test_db()
def query_api(category,tags):
	c = conn.cursor()
	placeholder= '?' # For SQLite. See DBAPI paramstyle.
	placeholders= ', '.join(placeholder for unused in tags)
	choices = fetchall_to_list(c.execute('SELECT * FROM TAGS'),0)
	fuzzed_tags = ()
	print "table"
	print_table('api_providers')
	print choices
	for i in tags:
		fuzzed = process.extractOne(i,choices)[0]
		fuzzed_tags+=(fuzzed,)
	intersect_string = '''SELECT api_endpoints.*
					FROM tagmap, api_endpoints, tags
					WHERE tags.rowid = tagmap.tag_id
					AND api_endpoints.category = (?)
					AND (tags.tag_name IN (''' + placeholders + '''))
					AND api_endpoints.rowid = tagmap.api_id
					GROUP BY api_endpoints.rowid
					HAVING COUNT( api_endpoints.rowid )=(?)'''
	query_rows = c.execute(intersect_string, (category,) + fuzzed_tags + (len(fuzzed_tags),))
	filtered_rows = []

	for row in query_rows:
		filtered_rows.append([row[2]])
	return filtered_rows
def fetchall_to_list(query_rows,col):
	filtered_rows = []
	for row in query_rows:
		filtered_rows.append(row[col])
	return filtered_rows

# print ("got " + str(query_api('stocks',('Symbol',))))
