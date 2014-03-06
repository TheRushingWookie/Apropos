import json
import urllib2
import sys
import proxy
import logging
import os
dir = os.getcwd()
'''"http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22YHOO%22,%22GOOG%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json"'''
print dir
class YahooStocks(proxy.proxy):
      provider_key = 'ffdf55ee-ebb5-4fb7-86e2-3932cb6764b6'
      provider_name = 'Example_provider'
      domain_name = "http://localhost:5000/"
      api_name = 'YahooStocks'
	output_tag_paths = {'Days High': ['query', 'results', 'quote', 'DaysHigh'], 'Last Trade Date': ['query', 'results', 'quote', 'LastTradeDate'], 'Book Value': ['query', 'results', 'quote', 'BookValue'], 'Percent Change From Two Hundred day Moving Average': ['query', 'results', 'quote', 'PercentChangeFromTwoHundreddayMovingAverage'], 'asking price': ['query', 'results', 'quote', 'Ask'], 'Fifty day Moving Average': ['query', 'results', 'quote', 'FiftydayMovingAverage'], 'Change From Year High': ['query', 'results', 'quote', 'ChangeFromYearHigh'], 'Stock Exchange': ['query', 'results', 'quote', 'StockExchange'], 'Price Earning Growth Ratio': ['query', 'results', 'quote', 'PEGRation'], 'EBITDA': ['query', 'results', 'quote', 'EBITDA'], 'Change From Fifty day Moving Average': ['query', 'results', 'quote', 'ChangeFromFiftydayMovingAverage'], 'Average Daily Volume': ['query', 'results', 'quote', 'AverageDailyVolume'], 'Two Hundred day Moving Average': ['query', 'results', 'quote', 'TwoHundreddayMovingAverage'], 'Percent Change From Fifty day Moving Average': ['query', 'results', 'quote', 'PercentChangeFromFiftydayMovingAverage'], 'Symbol': ['query', 'results', 'quote', 'Symbol'], 'Price To Book Ratio': ['query', 'results', 'quote', 'PriceBook'], 'Previous Close Price': ['query', 'results', 'quote', 'PreviousClosePrice'], 'Open Price': ['query', 'results', 'quote', 'OpenPrice'], 'Volume': ['query', 'results', 'quote', 'Volume'], 'Short Ratio': ['query', 'results', 'quote', 'ShortRatio'], 'Change From Year Low': ['query', 'results', 'quote', 'ChangeFromYearLow'], 'Days Low': ['query', 'results', 'quote', 'DaysLow'], 'Year Range': ['query', 'results', 'quote', 'YearRange'], 'Change': ['query', 'results', 'quote', 'ChangeRealtime'], 'Percent Change From Year High': ['query', 'results', 'quote', 'PercebtChangeFromYearHigh'], 'Stock Name': ['query', 'results', 'quote', 'Name'], 'Year High': ['query', 'results', 'quote', 'YearHigh'], 'Change From Two Hundred day Moving Average': ['query', 'results', 'quote', 'ChangeFromTwoHundreddayMovingAverage'], 'Percent Change From Year Low': ['query', 'results', 'quote', 'PercentChangeFromYearLow'], 'Last Trade Time': ['query', 'results', 'quote', 'LastTradeTime'], 'Price To Sales Ratio': ['query', 'results', 'quote', 'PriceSales'], 'Year Low': ['query', 'results', 'quote', 'YearLow'], 'Price Earnings Ratio': ['query', 'results', 'quote', 'PERation'], 'Market Capitalization': ['query', 'results', 'quote', 'MarketCapitalization'], 'Change in Realtime': ['query', 'results', 'quote', 'ChangeRealtime'], 'Last Trade Price': ['query', 'results', 'quote', 'LastTradePriceOnly'], 'Bid': ['query', 'results', 'quote', 'Bid'], 'Earnings per Share': ['query', 'results', 'quote', 'EarningsShare']}
      input_tags = ['stock_symbol']
	def __init__ (self):
            self.write_config()
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
	def get_stock_info(self, json_input):
		base_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22'
		part2 = '%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json'
		json_output = ""
		if "stock_symbol" in json_input['input']:
			base_url = base_url + urllib2.quote(json_input['input']['stock_symbol']) + part2
		else:
			raise Exception("Wrong Input Parameter " + base_url)
		#print base_url
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			json_output = opener.open(base_url).read()
		except:
			raise Exception("Output is " +  json_output)

		print str(json_output)
		standard_dict = standardize_output(json_output)
        final = {}
        for key in json:
            final[key] = standard_dict[key]
		return final


	def standardize_output(response):
		response = response['query']['results']['quote']
        if isinstance(response, dict):
            standard_output = {'price_to_book_ratio': response['PriceBook'],
                               'price_earning_growth_ratio': response['PEGRation'],
                               'average_daily_volume': response['AverageDailyVolume'],
                               'year_high': response['YearHigh'],
                               'change_in_realtime': response['ChangeRealtime'],
                               'year_range': response['YearRange'],
                               'ebitda': response['EBITDA'],
                               'stock_exchange': response['StockExchange'],
                               'change_from_year_low': response['ChangeFromYearLow'],
                               'change_from_year_high': response['ChangeFromYearHigh'],
                               'change_from_two_hundred_day_moving_average': response['ChangeFromTwoHundreddayMovingAverage'],
                               'percent_change_from_year_high': response['PercebtChangeFromYearHigh'],
                               'price_to_sales_ratio': response['PriceSales'],
                               'change': response['ChangeRealtime'],
                               'price_earnings_ratio': response['PERation'],
                               'fifty_day_moving_average': response['FiftydayMovingAverage'],
                               'stock_symbol': response['Symbol'],
                               'book_value': response['BookValue'],
                               'year_low': response['YearLow'],
                               'asking_price': response['Ask'],
                               'change_from_fifty_day_moving_average': response['ChangeFromFiftydayMovingAverage'],
                               'volume': response['Volume'],
                               'two_hundred_day_moving_average': response['TwoHundreddayMovingAverage'],
                               'open_price': response['OpenPrice'],
                               'last_trade_date': response['LastTradeDate'],
                               'market_capitalization': response['MarketCapitalization'],
                               'change_in_percent': response['ChangeinPercent'],
                               'stock_name': response['Name'],
                               'percent_change_from_year_low': response['PercentChangeFromYearLow'],
                               'last_trade_price': response['LastTradePriceOnly'],
                               'bid': response['Bid'],
                               'earnings_per_share': response['earningspershare'],
                               'previous_close_price': response['PreviousClosePrice'],
                               'short_ratio': response['ShortRatio'],
                               'percent_change_from_two_hundred_day_moving_average': response['       PercentChangeFromTwoHundreddayMovingAverage'],
                               'days_low': response['DaysLow'],
                               'last_trade_time': response['LastTradeTime'],
                               'days_high': response['DaysHigh'],
                               'percent_change_from_fifty_day_moving_average': response['PercentChangeFromFiftydayMovingAverage']}
		for key in response:
			if key == 'symbol':
				standard_output['stock_symbol'] == response[key]


	def init_actions(self):
		# need sample json input
		return {'stocks': self.get_stock_info}

''''"asking price": "33.25",
"Average Daily Volume": "16519500",
"Bid": "32.14",
"Book Value": "11.994",
"Last Trade Date": "10/25/2013",
"Earnings per Share": "1.159",
"Days Low": "32.00",
"Days High": "32.95",
"Year Low": "15.55",
"Year High": "30.27",
"Market Capitalization": "33.595B",
"EBITDA": "1.187B",
"Change From Year Low": "+16.70",
"Percent Change From Year Low": "+107.40%",
"Change From Year High": "+1.98",
"PercebtChangeFromYearHigh": "+6.54%",
"Fifty day Moving Average": "27.9089",
"Two Hundred day Moving Average": "25.7508",
"Change From Two Hundred day Moving Average": "+6.4992",
"Percent Change From Two Hundred day Moving Average": "+25.24%",
"Change From Fifty day Moving Average": "+4.3411",
"Percent Change From Fifty day Moving Average": "+15.55%",
"Stock Name": "Yahoo! Inc.",
"Open Price": "32.40",
"Previous Close Price": "33.08",
"Percent Change In Price": "-2.51%",
"Price To Sales Ratio": "7.24",
"Price To Book Ratio": "2.76",
"Price Earnings Ratio": "28.54",
"Price Earning Growth Ratio": "1.79",
"Symbol": "YHOO",
"Short Ratio": "1.40",
"Last Trade Time": "4:00pm",
"Volume": "22295864",
"Year Range": "15.55 - 30.27",
"Stock Exchange": "NasdaqNM",'''
