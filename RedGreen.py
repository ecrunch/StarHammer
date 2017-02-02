import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
import pdb

db = pymongo.MongoClient('localhost', 27017).Batman
pulled_date=datetime.today()

temp=db.stock.find()
stock = list(temp)

for t in stock:
	for s in t['Historical_Data']:
		if s['open_percent'] < s['close_percent']:
			