import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
from pullcount import pullcount 

db = pymongo.MongoClient('localhost', 27017).Batman

current = datetime.today()
import csv
with open('S&P_500.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	sign=str(row[0])
    	stock = Share(sign)
    	tracker = pullcount(current)
    	new_stock ={"Symbol": str(row[0]),"Name": str(stock.get_name()),"Last_Date": str(stock.get_trade_datetime()),"Historical_Data": []}
    	db.stock.update({"Symbol": str(row[0]), "Name": str(stock.get_name())}, new_stock, True)
    	old_date = (current - timedelta(days=40)).strftime('%Y-%m-%d')
    	historical_data=stock.get_historical(old_date, tracker.today_date)
    	for s in historical_data:
	    	s['total_movement'] = float(s['High']) - float(s['Low'])
	    	s['open_movement'] = float(s['Open']) - float(s['Low'])
	    	s['close_movement'] = float(s['Close']) - float(s['Low'])

	    	

	    	if s['total_movement'] !=0:	    
	    		s['open_percent'] = s['open_movement']/s['total_movement']
	    		s['close_percent'] = s['close_movement']/s['total_movement']

	    	db.stock.update({"Symbol": s["Symbol"]}, {'$push':{'Historical_Data':{'$each':[s] , '$position':0}}},upsert=True,multi=True)

