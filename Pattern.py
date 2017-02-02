import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
import pdb

db = pymongo.MongoClient('localhost', 27017).Batman
pulled_date=datetime.today()

temp=db.quandl_stock.find()
stock = list(temp)

for t in stock:
	for s in t['Historical_Data']:
		if len(s) > 10:
			if s['open_percent'] < .50 and s['close_percent'] < .50:
				if s['open_percent'] < .20 and s['close_percent'] < .20:
					s['Pattern'] = 'Shooting Star'
					s['Pattern_Strength'] = 'Strong'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)

				elif s['open_percent'] < .35 and s['close_percent'] < .35:
					s['Pattern'] = 'Shooting Star'
					s['Pattern_Strength'] = 'Medium'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)

				elif s['open_percent'] < .50 and s['close_percent'] < .50:
					s['Pattern'] = 'Shooting Star'
					s['Pattern_Strength'] = 'Weak'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)

			elif s['open_percent'] > .50 and s['close_percent'] > .50:
				if s['open_percent'] > .80 and s['close_percent'] > .80:
					s['Pattern'] = 'Hammer'
					s['Pattern_Strength'] = 'Strong'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)
					pprint.pprint(s)
				elif s['open_percent'] > .65 and s['close_percent'] > .65:
					s['Pattern'] = 'Hammer'
					s['Pattern_Strength'] = 'Medium'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)

				elif s['open_percent'] > .50 and s['close_percent'] > .50:
					s['Pattern'] = 'Hammer'
					s['Pattern_Strength'] = 'Weak'
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
					db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)

			else:	
				s['Pattern'] = 'none'
				s['Pattern_Strength'] = 'none'

				db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern':s['Pattern']}},upsert=False,multi=True)
				db.quandl_stock.update({"Symbol": t["Symbol"], 'Historical_Data.Date': s['Date']}, {'$set':{'Historical_Data.$.Pattern_Strength':s['Pattern_Strength']}},upsert=False,multi=True)


	    	