import sqlite3
from time import gmtime, strftime
conn = sqlite3.connect('apis.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE apis
             (date text, api_name text, api_key text, tags text)''')

# Insert a row of data
time = strftime("%a, %d %b %Y %X +0000", gmtime())
c.execute("insert into apis values (?, ?, ?)", (time, "test_api", "123712371273", "weather,temperature,") )
# Save (commit) the changes	
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()