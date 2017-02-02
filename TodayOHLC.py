import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
from pullcount import pullcount 

db = pymongo.MongoClient('localhost', 27017).Batman

current = datetime.today().strftime('%Y-%m-%d')
print current[:4]
print current [-2:]
print current [5:-3]

current = datetime(int(current[:4]),int(current [5:-3]), int(current [-2:]), 21)
print current

import csv
with open('S&P_500.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	print row
    	sign=str(row[0])
    	stock = Share(sign)
    	wcount = 0
    	while stock.get_trade_datetime() < current.strftime('%Y-%m-%d %H:%M'):
    		if wcount > 25:
    			break
    		stock.refresh()
    		wcount += 1
    	print stock.get_trade_datetime()
    	new_stock = {
    		"Volume" : stock.get_volume(),
			"Symbol" : str(sign),
			"High" : stock.get_days_high(),
			"Low" : stock.get_days_low(),
			"Date" : current.strftime('%Y-%m-%d'),
			"Pulled_datetime": stock.get_trade_datetime(),
			"Close" : stock.get_price(),
			"Open" : stock.get_open(),
    	}
    	new_stock['total_movement'] = float(new_stock['High']) - float(new_stock['Low'])
    	new_stock['open_movement'] = float(new_stock['Open']) - float(new_stock['Low'])
    	new_stock['close_movement'] = float(new_stock['Close']) - float(new_stock['Low'])
    	if new_stock['total_movement'] !=0:
    		new_stock['open_percent'] = new_stock['open_movement']/new_stock['total_movement']
    		new_stock['close_percent'] = new_stock['close_movement']/new_stock['total_movement']

    	db.stock.update({"Symbol": new_stock["Symbol"]}, {'$addToSet':{'Historical_Data':new_stock}},upsert=True,multi=True)

    	print new_stock
   #  	db.stock.update({"Symbol": str(row[0]), "Name": str(stock.get_name())}, new_stock, True)
   #  	old_date = (current - timedelta(days=40)).strftime('%Y-%m-%d')
   #  	historical_data=stock.get_historical(old_date, tracker.today_date)