# -*- coding: UTF-8 -*-
import sys
import os
import pymongo

fr = open("factor.txt","r")
lines = fr.readlines()

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['test']

data = {}
for line in lines:
	key =  line.split()[0]
	value = line.split()[1]
	data[key] = value

collection.insert(data)
