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
# print pullcount(pulled_date)

temp=db.quandl_stock.find({ 'Historical_Data': { '$all': [{'$elemMatch': {'Pattern': 'Hammer'}}]}})
hammer = list(temp)
# print hammer

for t in hammer:
	Hist_array = 0
	for s in t['Historical_Data']:
		# print t["Symbol"]
		# print t['Symbol']
		# print s
		
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
			if len(streak_type_arr) > 2: 
				print t['Symbol']
				print pattern_date
				print streak_type_arr

				db.quandl_stock.update({'Symbol':t['Symbol'], 'Historical_Data.Date': pattern_date},{'$set':{'Historical_Data.$.streak': len(streak_type_arr)}}, False,True)
				for i in streak_type_arr:	
					db.quandl_stock.update({'Symbol':t['Symbol'], 'Historical_Data.Date': pattern_date},{'$inc':{'Historical_Data.$.streak_arr_str': streak_type_arr[i]}}, False,True)

		Hist_array += 1
		# and datetime(int((s['Date'][:4])),int((s['Date'][5:-3])),int((s['Date'][-2:]))) > datetime(2017,01,13)):

			
			





				

			




