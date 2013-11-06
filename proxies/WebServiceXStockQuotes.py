import requests
import xml.etree.ElementTree as ET
import proxy
import HTMLParser
class WebServiceXStockQuotes(proxy.proxy):
	json_output_name_map = {'Volume': 'Volume', 'Last Trade Price': 'LastTradePrice', 'Stock Name': 'Name', 'P-E': 'PERation','Price Earnings Ratio': 'PERation', 'Symbol': 'Symbol','Previous Close Price': 'PreviousClosePrice', 'PreviousClose': 'PreviousClosePrice', 'Days High': 'DaysHigh','High': 'DaysHigh', 'PercentageChange': 'ChangeinPercent','Change in percent':'ChangeinPercent', 'Days Low': 'DaysLow','Low': 'DaysLow', 'Last Trade Time': 'LastTradeTime','Time': 'LastTradeTime', 'Last Trade Date': 'LastTradeDate','Date': 'LastTradeDate', 'Earns': 'earningspershare', 'Earnings per Share': 'earningspershare','MktCap': 'MarketCapitalization', 'Open Price': 'OpenPrice', 'Open': 'OpenPrice','Year Range': 'YearRange', 'AnnRange': 'YearRange', 'Market Capitalization': 'MarketCapitalization','Change': 'ChangeRealtime','Change in Realtime':'ChangeRealtime'}
							
	json_name_to_path_map ={'Volume': ['Volume'], 'LastTradeDate': ['Date'], 'MarketCapitalization': ['MktCap'], 'DaysHigh': ['High'], 'PreviousClosePrice': ['PreviousClose'], 'Symbol': ['Symbol'], 'YearRange': ['AnnRange'], 'OpenPrice': ['Open'], 'earningspershare': ['Earns'], 'LastTradeTime': ['Time'], 'DaysLow': ['Low'], 'LastTradePrice': ['Last'], 'ChangeRealtime': ['Change'], 'ChangeinPercent': ['PercentageChange'], 'PERation': ['P-E'], 'Name': ['Name']}


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
		print json_input['input']['stock_symbol']
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