import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
import pdb
from pullcount import pullcount 

db = pymongo.MongoClient('localhost', 27017).Batman
pulled_date=datetime.today()
print pullcount(pulled_date)

temp=db.stock.find()
stock = list(temp)

for t in stock:
	high = 0
	high_date =''
	low=0
	low_date=''
	past_high =''
	past_low = ''
	for s in t['Historical_Data']:
		if (past_high == '' and past_low == ''):
			past_high = s['High']
			past_low = s['Low']
			high_date = s['Date']
			low_date = s['Date']
		elif past_high < s['High']:
			past_high = s['High']
			high_date = s['Date']
		elif past_low > s['Low']:
			past_low  = s['Low']
			low_date = s['Date']
	print past_low
	print low_date
	print past_high
	print high_date 
	print t['Symbol']
	db.stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': low_date}, {'$set':{'Historical_Data.$.Historical_Low':1}},upsert=False,multi=True)
	db.stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': high_date}, {'$set':{'Historical_Data.$.Historical_High':1}},upsert=False,multi=True)






