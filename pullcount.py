import pymongo
import json
from yahoo_finance import Share
from datetime import datetime, timedelta
import pprint
from bson import json_util
import pdb

db = pymongo.MongoClient('localhost', 27017).Batman
pulled_date=datetime.today()

class pullcount:
	
	print pulled_date.strftime('%Y-%m-%d')
	def __init__(self, pulled_date):
		pulled_date=datetime.today()
		self.today_date = datetime.today()
		self.today_date = str(pulled_date.strftime('%Y-%m-%d'))
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