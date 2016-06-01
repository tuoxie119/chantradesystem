import pymongo
import tushare as ts
import re

conn = ''

def getconn():
    return pymongo.MongoClient('192.168.222.188', port=27017)

