import pymongo
import json
from bson import json_util
import requests
db = pymongo.MongoClient('localhost', 27017).Batman
from datetime import datetime, timedelta
import pprint

first_part = "https://www.quandl.com/api/v3/datasets/"
last_part = "/data.json?limit=1&api_key=Q7DSNVGYPQ9WnMmxEgVb"

current = datetime.today()
import csv
with open('WIKI-datasets-codes.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            data_set_code = str(row[0])
            symbol = data_set_code[5:len(data_set_code)]
            print symbol
            link = first_part + str(row[0]) + last_part
            r = requests.get(link)
            quandl_stock_json = r.json()
            last_date = quandl_stock_json["dataset_data"]["data"][0][0]
            print last_date
            print current
            daydiff = (current - datetime.strptime(last_date,"%Y-%m-%d"))
            print daydiff
            if daydiff.days == 3:
                print "Here"
                db.workingstock.insert_one({"Symbol": str(symbol), "Date":str(last_date)})
                print "success"
        except:
            continue
            


     
    
    
