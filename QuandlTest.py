#!/usr/bin/python
#import quandl
#quandl.ApiConfig.api_key ='Q7DSNVGYPQ9WnMmxEgVb'
import pprint
import pymongo
import pdb
#import pandas
import json
from bson import json_util
import requests
db = pymongo.MongoClient('localhost', 27017).Batman
from datetime import datetime, timedelta

# mydata = quandl.get("WIKI/KR")

# pdb.set_trace()

# listKR =mydata.to_list()

WIKI ="WIKI/"
first_part = "https://www.quandl.com/api/v3/datasets/WIKI/"
last_part = "/data.json?limit=6&api_key=Q7DSNVGYPQ9WnMmxEgVb"

# link = first_part + "BRK" + last_part
# r = requests.get(link)
# quandl_stock_json = r.json()
# print quandl_stock_json
current = datetime.today()
import csv
with open('S&P_500.csv', 'rb') as f:
	 reader = csv.reader(f)
	 for row in reader:
	 	data_set_code = str(row[0])
	 	print data_set_code
	 	symbol = data_set_code
	 	link = first_part + str(row[0]) + last_part
	 	r = requests.get(link)
	 	pprint.pprint(r) 
	 	quandl_stock_json = r.json()
	 	length=len(quandl_stock_json["dataset_data"]["data"])
	 	print length
	 	testm =  current - datetime.strptime(quandl_stock_json["dataset_data"]["data"][1][0],"%Y-%m-%d")
	 	if testm.days < 5 and length != 0:
	 		db.quandl_stock.update({"Symbol": str(symbol)}, {"Symbol": str(symbol), "Historical_Data": []}, True)

		 	for i in range(0,length):
		 		
		 		new={
		 			"Date":quandl_stock_json["dataset_data"]["data"][i][0],
		 			"Open":quandl_stock_json["dataset_data"]["data"][i][1],
		 			"High":quandl_stock_json["dataset_data"]["data"][i][2],
		 			"Low":quandl_stock_json["dataset_data"]["data"][i][3],
		 			"Close":quandl_stock_json["dataset_data"]["data"][i][4],
		 			"Volume":quandl_stock_json["dataset_data"]["data"][i][5]
		 		}
		 		print new['High']
		 		print quandl_stock_json["dataset_data"]["data"][i]
		 		new['total_movement'] = float(new['High']) - float(new['Low'])
		 		new['open_movement'] = float(new['Open']) - float(new['Low'])
		 		new['close_movement'] = float(new['Close']) - float(new['Low'])
		 		if new['total_movement'] !=0:
		 			new['open_percent'] = new['open_movement']/new['total_movement']
		 			new['close_percent'] = new['close_movement']/new['total_movement']
		 		print new
		 		db.quandl_stock.update({"Symbol": symbol}, {'$push':{'Historical_Data':{'$each':[new]}}},upsert=True,multi=True)





# test = quandl.get("WIKI/KR", limit = 30)
# # print test
# # pdb.set_trace()
# # test = test.to_dict()
# test = test.to_json(orient='records')[1:-1].replace('},{', '} {')
# # test = test.to_json()
# test = json.dumps(test)
# print test 
# for t in test:
# 	print t

# testt= quandl.Dataset('WIKI/AAPL').data(params={ 'limit': 1 })[0]


# iport csv
# with open(test, 'rb') as f:
# 	reader = csv.reader(f)
# 	for row in reader:
# 		print row[0]

# for i in test:
# 	# pdb.set_trace()
# 	print i.value







# import csv
# with open('S&P_500.csv', 'rb') as f:
# 	 reader = csv.reader(f)
# 	 for row in reader:
# 	 	data_set_code = str(WIKI + row[0])
# 	 	print data_set_code
# 	 	symbol = row[0]
# 	 	print symbol
# # 	 	quandl_stock_dataset = quandl.get(data_set_code,limit = 30)
# # 	 	quandl_stock_dataset_list=list(quandl_stock_dataset)
# # 	 	quandl_stock_dataset_len = len(quandl_stock_dataset)
# # 	 	# pdb.set_trace()
# # 	 	quandl_stock_dataset_list = quandl_stock_dataset.to_list()
# # 	 	for i in range(0, quandl_stock_dataset_len):
# # 	 		print quandl_stock_dataset[i]

# 	 	db.quandl_stock.update({"Symbol": str(symbol)}, {"Symbol": str(symbol), "Historical": []}, True)
# 	 	# for d in range(0,quandl_stock_dataset_len):
# 	 	# 	stock = {
# 	 	# 	'Date': str(quandl_stock_dataset[d].date),
	 	# 	'Open': quandl_stock_dataset[d].open,
	 	# 	'High': quandl_stock_dataset[d].high,
	 	# 	'Low': quandl_stock_dataset[d].low,
	 	# 	'Close': quandl_stock_dataset[d].close,
	 	# 	'Volume': quandl_stock_dataset[d].volume
	 	# 	}

	 	# 	print stock
	 	# 	print symbol
	 	# 	






# sh = quandl.Dataset('WIKI/KR').data()

# test = int(len(sh)) - 1
# stock_day = []

# for i in range(0,test):
# 	stock = {
# 	'Date': str(sh[i-1].date),
# 	'Open': sh[i-1].open,
# 	'High': sh[i-1].high,
# 	'Low': sh[i-1].low,
# 	'Close': sh[i-1].close,
# 	'Volume': sh[i-1].volume
# 	}

# 	pprint.pprint(stock)






