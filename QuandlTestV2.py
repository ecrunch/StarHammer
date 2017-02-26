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

from twilio.rest import TwilioRestClient

account_sid = "AC63f80ff8943bb80479f0be17b7542b41" # Your Account SID from www.twilio.com/console
auth_token  = "f111e11d311c51764c0251b300dfd6c4"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

WIKI ="WIKI/"
first_part = "https://www.quandl.com/api/v3/datasets/WIKI/"
last_part = "/data.json?limit=6&api_key=Q7DSNVGYPQ9WnMmxEgVb"

# link = first_part + "BRK" + last_part
# r = requests.get(link)
# quandl_stock_json = r.json()
# print quandl_stock_json
current = datetime.today()
cursor = db.workingstock.find({})
#pdb.set_trace()
errorCount = 0
count = 1
for document in cursor:
        print count
	count =count +1
	pprint.pprint(str(document['Symbol']))
	symbol = str(document['Symbol'])
	link = first_part + symbol + last_part
	try:
		r = requests.get(link)
		quandl_stock_json = r.json()
		length=len(quandl_stock_json["dataset_data"]["data"])
		testm =  current - datetime.strptime(quandl_stock_json["dataset_data"]["data"][1][0],"%Y-%m-%d")
		if testm.days < 6 and length != 0:
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
				else:
                                        new['open_percent'] = 0
					new['close_percent'] = 0
				print new
                                if new['open_percent'] < .50 and new['close_percent'] < .50:
                                        if new['open_percent'] < .20 and new['close_percent'] < .20:
                                                new['Pattern'] = 'Shooting Star'
                                                new['Pattern_Strength'] = 'Strong'
                                                
                                        elif new['open_percent'] < .35 and new['close_percent'] < .35:
                                                new['Pattern'] = 'Shooting Star'
                                                new['Pattern_Strength'] = 'Medium'
                                                
                                        elif new['open_percent'] < .50 and new['close_percent'] < .50:
                                                new['Pattern'] = 'Shooting Star'
                                                new['Pattern_Strength'] = 'Weak'
                                                
                                elif new['open_percent'] > .50 and new['close_percent'] > .50:
                                        if new['open_percent'] > .80 and new['close_percent'] > .80:
                                                new['Pattern'] = 'Hammer'
                                                new['Pattern_Strength'] = 'Strong'
                                        elif new['open_percent'] > .65 and new['close_percent'] > .65:
                                                new['Pattern'] = 'Hammer'
                                                new['Pattern_Strength'] = 'Medium'
                                                
                                        elif new['open_percent'] > .50 and new['close_percent'] > .50:
                                                new['Pattern'] = 'Hammer'
                                                new['Pattern_Strength'] = 'Weak'
                                                
                                else:	
                                        new['Pattern'] = 'none'
                                        new['Pattern_Strength'] = 'none'
                                print 'here'
                                pprint.pprint(new)
				db.quandl_stock.update({"Symbol": symbol}, {'$push':{'Historical_Data':{'$each':[new]}}},upsert=True,multi=True)
	except:
		errorCount = errorCount +1
		continue
	
temp=db.quandl_stock.find({ 'Historical_Data': { '$all': [{'$elemMatch': {'Pattern': 'Hammer'}}]}})
hammer = list(temp)
# print hammer

for t in hammer:
	Hist_array = 0
	try:
		for s in t['Historical_Data']:
		
			if s['Pattern'] == 'Hammer' and (s['Pattern_Strength'] == 'Strong' or s['Pattern_Strength'] == 'Medium'):
				pattern_date = s['Date']
				pattern_high = s['High']
				pattern_low = s['Low']
				pattern_open = s['Open']
				pattern_close = s['Close']
				streak_type_arr =[]
				past_date = []


				if (Hist_array+30) > len(t['Historical_Data']):
					Hist_till_array = (len(t['Historical_Data']) -1)
				else:
					Hist_till_array = Hist_array + 30
				
				for r in range(Hist_array+1, Hist_till_array): 
					temp=t['Historical_Data'][r]
					if temp['Date'] < pattern_date:
						past_date.append([temp['Date'],temp['High'], temp['Low'],temp['Open'],temp['Close']])
				streak = 0

				for u in past_date:
					if streak > 0:
						if streak_open < u[3] and streak_close < u[4] and streak_open < u[4] and streak_close < u[3]:
							streak_type = 2
							streak_type_arr.append(streak_type)
							streak_date=u[0]
							streak_high=u[1]
							streak_low=u[2]
							streak_open=u[3]
							streak_close=u[4] 
							streak =1
						elif (streak_close < u[3] and streak_close < u[4]) or (streak_open < u[3] and streak_open < u[4]):
							streak_type = 1
							streak_type_arr.append(streak_type)
							streak_date=u[0]
							streak_high=u[1]
							streak_low=u[2]
							streak_open=u[3]
							streak_close=u[4] 
							streak =1
						else: 
							streak_type = 0
							
							break	

					else:
						if pattern_open < u[3] and pattern_close < u[4] and pattern_open < u[4] and pattern_close < u[3]:
							streak_type = 2
							streak_type_arr.append(streak_type)
							streak_date=u[0]
							streak_high=u[1]
							streak_low=u[2]
							streak_open=u[3]
							streak_close=u[4] 
							streak =1
						elif (pattern_close < u[3] and pattern_close < u[4]) or (pattern_open < u[3] and pattern_open < u[4]):
							streak_type = 1
							streak_type_arr.append(streak_type)
							streak_date=u[0]
							streak_high=u[1]
							streak_low=u[2]
							streak_open=u[3]
							streak_close=u[4] 
							streak =1
						else: 
							streak_type = 0
							break
				yester = current - datetime.strptime(pattern_date,"%Y-%m-%d")
				if len(streak_type_arr) > 2 and yester.days == 2: 
					print t['Symbol']
					print pattern_date
					print streak_type_arr
					text_message = "|||" + str(s['Close']) + " " + str(t['Symbol']) + " " + str(pattern_date) + " " + str(streak_type_arr) + "|||"
					       
					
					message = client.messages.create(body=text_message,
					   to="+13125689880",    # Replace with your phone number
					   from_="+16305604797") # Replace with your Twilio number
					   
					print(message.sid)

					text_message = ""
					
			Hist_array += 1
	except:
		errorCount = errorCount +1
		continue
			
		# and datetime(int((s['Date'][:4])),int((s['Date'][5:-3])),int((s['Date'][-2:]))) > datetime(2017,01,13)):
print "Errors Handled: " + str(errorCount)


	    	


