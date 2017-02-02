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


current = datetime.today()
pastday = (current - timedelta(days=1)).strftime('%Y-%m-%d')
secondday = (current - timedelta(days=5)).strftime('%Y-%m-%d')
thirdday = (current - timedelta(days=6)).strftime('%Y-%m-%d')
fourthday = (current - timedelta(days=7)).strftime('%Y-%m-%d')
fifthday = (current - timedelta(days=8)).strftime('%Y-%m-%d')
current = current.strftime('%Y-%m-%d')


print current
print pastday
print secondday
print thirdday
print fourthday
print fifthday

import csv
with open('S&P_500.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	
    	# pdb.set_trace()
    	fifthdayPosition =  db.stock.find({ 'Symbol': row[0]})
    	fifthdayPosition = list(fifthdayPosition)
    	fifthdayPosition = fifthdayPosition[0]
    	fifthdayPosition = fifthdayPosition['Historical_Data']
    	tracked_pattern = 'N'
    	streak = 0
    	for f in fifthdayPosition:

    		# past_drop_streak =
    		total_movement = float(f['High']) - float(f['Low'])
    		open_movement = float(f['Open']) - float(f['Low'])
    		close_movement = float(f['Close']) - float(f['Low'])
    		open_percent = open_movement/total_movement
    		close_percent = close_movement/total_movement
    		if  tracked_pattern ==	 'N':	
	    		if open_percent < .50 and close_percent < .50:
	    			tracked_pattern = 'SS'
	    			print 'Shooting Star'
	    			print f['Symbol']
	    			print f['Date']
	    			f['Pattern'] = 'Shooting Star'

	    		elif open_percent > .50 and close_percent > .50:
	    			tracked_pattern = 'H'
	    			print 'Hammer'
	    			print f['Symbol']
	    			print f['Date']
	    			f['Pattern'] = 'Hammer'
	    		else :
	  				tracked_pattern = 'N'
	  				f['Pattern'] = 'none'

	    	elif tracked_pattern == 'H':
	    		if streak > 0:
	    			if f['Open'] > f['Close']:
	    				if past_close > f['Close']:
	    					streak += 1
	    					past_close = f['Close']
	    					print streak
	    				else:
	    					tracked_pattern = 'N'
	    					streak = 0
	    			else:
	    				streak = 0
	    				tracked_pattern = 'N'
	    		else:
	    			if f['Open'] > f['Close']:
	    				past_close = f['Close']
	    				tracked_pattern = 'H'
	    				streak = 1
