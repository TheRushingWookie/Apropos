import requests
import xml.etree.ElementTree as ET
import proxy
import HTMLParser
class WebServiceXStockQuotes(proxy.proxy):
	provider_key = 'ffdf55ee-ebb5-4fb7-86e2-3932cb6764b6'
	provider_name = ''
	domain_name = "http://localhost:5000/"
	api_name = 'WebServiceXStockQuotes'
	def __init__ (self):
		self.actions = self.init_actions()
		self.json_outputs = self.init_outputs()
	def custom_type_converter(self,val,val_type):
		converation_chars = {'B' : 1e9, 'M':1e6 }
		conversation_factor = 1
		if isinstance(val,str) and (val_type == 'int' or val_type == 'integer'):
			for i in converation_chars.keys():
				found = val.find(i)
				if found > -1:
					conversation_factor = converation_chars[i]
					return int(val[:found]) * conversation_factor
		return val
	def get_stock_info(self,json_input):
		r = requests.get('http://www.webservicex.net/stockquote.asmx/GetQuote', params = {'symbol':json_input['input']['stock_symbol']})
		h = HTMLParser.HTMLParser()
		decoded_string = h.unescape(r.text)
		json_output = {}
		xml = ET.fromstring(decoded_string)
		for i in range(len(xml[0][0])):
			json_output[xml[0][0][i].tag[len('{http://www.webserviceX.NET/}'):]] = xml[0][0][i].text
		print str(json_output)
		return json_output

	def init_actions(self):
		return {'stocks':self.get_stock_info}