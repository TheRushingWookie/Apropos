import re
class aql_selector:
	query_string = None
	data_source = None
	restrictions = []
	def __init__ (self, query_string, data_source):
		self.query_string = query_string
		self.data_source = data_source
def parse_aql_string (aql_string):
	aql_selector_instance = aql_selector(aql_string,None)
	tokenize_aql(aql_string,{"select":select, "from":from_1}, aql_selector_instance)
	print(aql_selector_instance.query_string)
def tokenize_aql (token_string,keyword_hash,aql_selector_obj):
	tokens = re.split("( )| \"", token_string)
	aql_keyword = ""
	in_quote = False
	start_offset = 0
	aql_keys_arr = []
	curr_funct  = None
	print(tokens)
	for token in tokens:
		token = token.lower()
		if token == "\"":
			if in_quote:
				in_quote = False
			else:
				in_quote = True
		if in_quote:
			None
		else:
			if token in keyword_hash:
				curr_funct = keyword_hash[token]
				curr_funct()
def select ():
	print(" IN SELecTING")
def from_1 ():
	print("hello")
parse_aql_string("Select \" DONT EVAL ME Select \" from x")