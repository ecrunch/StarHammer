from flask import Flask, jsonify, Response, request
import pymongo
import json
import praw
import obot
import pprint
from bson import json_util
import pdb
from yql.api import YQL
from yahoo_finance import Share
from datetime import datetime, timedelta


#Setup Server
app = Flask(__name__)

#Setup Reddit Wrapper (praw)
r = praw.Reddit(user_agent=obot.app_ua)

#Setup db (pymongo)
db = pymongo.MongoClient('localhost', 27017).Batman

searches=[]



# pdb.set_trace()
stock_list = ['PTHN','GPRO','TSLA', 'UA']



#-----------------------
# Manage Date Manipulation

#----------------------- beginning
# today_date=datetime.today()
# old_date = (today_date - timedelta(days=30)).strftime('%Y-%m-%d')
# today_date = today_date.strftime('%Y-%m-%d')

# print today_date
# print old_date
#----------------------- end




#-----------------------
# get symbol and pattern from mongo
# 
#----------------------- beginning
# historical_stock = db.historical_stock
# taco=json_util.dumps(historical_stock.find({'Symbol':'TSLA','Pattern':'Shooting Star'}))

# pprint.pprint(taco)
#----------------------- end




#-----------------------
# get historical prices from yahoo finance 
# Adds pattern
#
#----------------------- beginning
# historical_data = []
# stock=Share('PTHN')
# print stock.get_price()

# historical_data=stock.get_historical(old_date, today_date)
# pprint.pprint(historical_data)


# for s in historical_data:
# 	total_movement = float(s['High']) - float(s['Low'])
# 	open_movement = float(s['Open']) - float(s['Low'])
# 	close_movement = float(s['Close']) - float(s['Low'])

# 	open_percent = open_movement/total_movement
# 	close_percent = close_movement/total_movement
	

# 	if open_percent < .30 and close_percent < .30:
# 		s['Pattern'] = 'Shooting Star'
# 	elif open_percent > .70 and close_percent > .70:
# 		s['Pattern'] = 'Hammer'
# 	else :
# 		s['Pattern'] = 'none'

	

# 	db.historical_stock.update({'Symbol': s['Symbol'], 'Date': s['Date']}, s, True)
 
#----------------------- end



#-----------------------
# get prices now from yahoo finance 
# Adds pattern
# !!!! sometimes returns wrong date
#----------------------- beginning
# for s in stock_list:
# 	stock=Share(s)
# 	new_stock = {
# 	"Name": str(stock.get_name()),
# 	"Price": str(stock.get_price()),
# 	"High": str(stock.get_days_high()),
# 	"Low": str(stock.get_days_low()),
# 	"Previous close": str(stock.get_prev_close()),
# 	"Open": str(stock.get_open()),
# 	"Volume": str(stock.get_volume()),
# # 	"Date": str(stock.get_trade_datetime())}

# 	total_movement = float(stock['High']) - float(stock['Low'])
# 	open_movement = float(stock['Open']) - float(stock['Low'])
# 	close_movement = float(stock['Close']) - float(stock['Low'])

# 	open_percent = open_movement/total_movement
# 	close_percent = close_movement/total_movement
	

# 	if open_percent < .30 and close_percent < .30:
# 		stock['Pattern'] = 'Shooting Star'
# 	elif open_percent > .70 and close_percent > .70:
# 		stock['Pattern'] = 'Hammer'
# 	else :
# 		stock['Pattern'] = 'none'


# 	db.stock.update({"name": str(stock.get_name()),"date": str(stock.get_trade_datetime())}, new_stock, True)

#----------------------- end

# m=datetime.today()
# time_track = {
# 			'Date': m.strftime('%Y-%m-%d'),
# 			'Hour': m.strftime('%H'),
# 			'Count': 0
# 		}


# db.pullcount.update({'Date':time_track['Date'],'Hour':time_track['Hour']},time_track,True)



current_searches=0

class pullcount:
	def __init__(self, pulled_date):
		self.today_date = pulled_date.strftime('%Y-%m-%d')
		self.hour = pulled_date.strftime('%H')
	
		if db.pullcount.find({'Date':self.today_date,'Hour':self.hour}).count() > 0:
			temp = db.pullcount.find_one({'Date':self.today_date,'Hour':self.hour})
			self.count_of_yahoo_pulls = temp['Count']
		else:
			self.count_of_yahoo_pulls = 0

		time_track = {
			'Date': self.today_date ,
			'Hour': self.hour,
			'Count': self.count_of_yahoo_pulls
		}
		db.pullcount.update({'Date':time_track['Date'],'Hour':time_track['Hour']},time_track,True)

	def add_search(self,symbol):

		def add_count():
			updated_count = (int(self.count_of_yahoo_pulls) + 1)
			request_track = {
				'Date': self.today_date,
				'Hour': self.hour,
				'Count': updated_count
			}
			db.pullcount.update({'Date':request_track['Date'],'Hour':request_track['Hour']},request_track,True)
		

		if (db.past_searches.find({'Symbol':symbol}).count() == 0):
			search = {
				'Symbol': symbol,
				'Date': self.today_date,
				'Hour': self.hour
			}
			db.past_searches.update({'Symbol': search['Symbol']},search,True)
			add_count()
			return True
		else:
			temp = db.past_searches.find_one({'Symbol':symbol})
			
			if (temp['Date'] < self.today_date and int(self.hour) > 18):
				search = {
				'Symbol': symbol,
				'Date': self.today_date,
				'Hour': self.hour
				}
				db.past_searches.update({'Symbol': search['Symbol']},search,True)
				add_count()
				return True
			else: 
				return False

# current = datetime.today()
# import csv
# with open('S&P_500.csv', 'rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#     	print row[0]
#     	sign=str(row[0])
#     	stock = Share(sign)
#     	tracker = pullcount(current)
#     	new_stock ={"Symbol": str(row[0]),"Name": str(stock.get_name()),"Last_Date": str(stock.get_trade_datetime()),"Historical_Data": []}
#     	db.stock.update({"Symbol": str(row[0]), "Name": str(stock.get_name())}, new_stock, True)
#     	old_date = (current - timedelta(days=365)).strftime('%Y-%m-%d')
#     	print tracker.today_date
#     	print old_date
#     	historical_data=stock.get_historical(old_date, tracker.today_date)
#     	for s in historical_data:
# 	    	total_movement = float(s['High']) - float(s['Low'])
# 	    	open_movement = float(s['Open']) - float(s['Low'])
# 	    	close_movement = float(s['Close']) - float(s['Low'])
# 	    	if total_movement !=0:	    
# 	    		open_percent = open_movement/total_movement
# 	    		close_percent = close_movement/total_movement

# 	    	if open_percent < .30 and close_percent < .30:
# 	    		s['Pattern'] = 'Shooting Star'
# 	    	elif open_percent > .70 and close_percent > .70:
# 	    		s['Pattern'] = 'Hammer'
# 	    	else :
# 	    		s['Pattern'] = 'none'
# 	    	open_percent=0
# 	    	close_percent=0

#     	for t in historical_data:
# 	    	pprint.pprint(t)
# 	    	print t['Symbol']
# 	    	db.stock.update({"Symbol": t["Symbol"]}, {'$addToSet':{'Historical_Data':t}},upsert=True,multi=True)






		

@app.route('/api/stocks')

def get_stocks():
	current = datetime.today()
	tracker=pullcount(current)
	search = list(db.stock.find())
	resp = json.dumps(search,default=json_util.default)
	return resp

@app.route('/api/get_stock', methods = ['post'])
def get_stock():
	current = datetime.today()
	tracker=pullcount(current)
	stockname = request.json
	symbol = str(stockname['Name'])
	stock=Share(symbol)
	new_stock = {
		"Symbol": str(symbol),
		"Name": str(stock.get_name()),
		"Last_Date": str(stock.get_trade_datetime()),
		"Historical_Data": []
	}
	db.stock.update({"Symbol": str(symbol), "Name": str(stock.get_name())}, new_stock, True)
	old_date = (current - timedelta(days=365)).strftime('%Y-%m-%d')
	historical_data=stock.get_historical(old_date, tracker.today_date)
	for s in historical_data:
		total_movement = float(s['High']) - float(s['Low'])
		open_movement = float(s['Open']) - float(s['Low'])
		close_movement = float(s['Close']) - float(s['Low'])

		open_percent = open_movement/total_movement
		close_percent = close_movement/total_movement
		

		if open_percent < .30 and close_percent < .30:
			s['Pattern'] = 'Shooting Star'
		elif open_percent > .70 and close_percent > .70:
			s['Pattern'] = 'Hammer'
		else :
			s['Pattern'] = 'none'
	for t in historical_data:
		pprint.pprint(t)
		print t['Symbol']

		db.stock.update({"Symbol": t["Symbol"]}, {'$addToSet':{'Historical_Data':t}},upsert=True,multi=True)

	return '"success"'

@app.route('/api/get_historical_data', methods = ['post'])
def get_historical_data():
	current = datetime.today()
	stockname = request.json
	tracker=pullcount(current)
	symbol = str(stockname['Name'])
	print symbol
	# tracker.add_search(symbol)
	if (True):
		old_date = (current - timedelta(days=30)).strftime('%Y-%m-%d')
		stock=Share(symbol)
		historical_data=stock.get_historical(old_date, tracker.today_date)

		for s in historical_data:
			total_movement = float(s['High']) - float(s['Low'])
			open_movement = float(s['Open']) - float(s['Low'])
			close_movement = float(s['Close']) - float(s['Low'])

			open_percent = open_movement/total_movement
			close_percent = close_movement/total_movement
			

			if open_percent < .30 and close_percent < .30:
				s['Pattern'] = 'Shooting Star'
			elif open_percent > .70 and close_percent > .70:
				s['Pattern'] = 'Hammer'
			else :
				s['Pattern'] = 'none'
		for t in historical_data:
			pprint.pprint(t)
			print t['Symbol']

			db.stock.update({"Symbol": t["Symbol"]}, {'$addToSet':{'Historical_Data':t}},upsert=True,multi=True)

		return '"success"'
	else:
		print 'up to date'
		return '"success"'


	

	


@app.route('/api/search', methods =['Post'])

def search_reddit():
	# pdb.set_trace()
	jname = request.json
	print jname
	name = str(jname['name'])
	print name
	redditSearch = r.search(name)
	for s in redditSearch:
	        new_post = {
	            "subreddit": str(s.subreddit ),
	            "title": str(s.title),
	            "author": str(s.author),
	            "created_utc": s.created_utc,
	            "url": str(s.url),
	            "search": str(name)
	        }


	        db.reddit.update({"url": str(s.url)}, new_post, True)

		return '"success"'

if __name__ == '__main__':
    app.run(debug = True)
