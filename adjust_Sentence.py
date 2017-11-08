#-*- coding:utf-8 -*-
from pymongo import MongoClient 

client = MongoClient('localhost',27017)
db = client['test']
collection = db['test']

dataInf = collection.find({})

map_min = {}
map_max = {}
map_min["14岁到16岁之间犯罪".decode("utf-8")] = -0.6
map_max["14岁到16岁之间犯罪".decode("utf-8")] = -0.3
map_min["16岁到18岁之间犯罪".decode("utf-8")] = -0.5
map_max["16岁到18岁之间犯罪".decode("utf-8")] = -0.1
map_min["未遂犯".decode("utf-8")] = -0.5
map_max["未遂犯".decode("utf-8")] = -0.5
map_min["从犯".decode("utf-8")] = -0.5
map_max["从犯".decode("utf-8")] = -0.2
map_min["自首".decode("utf-8")] = -0.4
map_max["自首".decode("utf-8")] = 0
map_min["一般立功".decode("utf-8")] = -0.2
map_max["一般立功".decode("utf-8")] = -0.2
map_min["重大立功".decode("utf-8")] = -0.5
map_max["重大立功".decode("utf-8")] = -0.2
map_min["坦白且如实供述".decode("utf-8")] = -0.2
map_max["坦白且如实供述".decode("utf-8")] = 0
map_min["坦白且如实供述司法机关未掌握的同种罪行".decode("utf-8")] = -0.3
map_max["坦白且如实供述司法机关未掌握的同种罪行".decode("utf-8")] = -0.1
map_min["坦白且如实供述避免严重后宫发生".decode("utf-8")] = -0.5
map_max["坦白且如实供述避免严重后宫发生".decode("utf-8")] = -0.3
map_min["当庭认罪".decode("utf-8")] = -0.1
map_max["当庭认罪".decode("utf-8")] = 0
map_min["积极赔偿但未取得被害人谅解".decode("utf-8")] = -0.3
map_max["积极赔偿但未取得被害人谅解".decode("utf-8")] = 0
map_min["积极赔偿并取得被害人谅解".decode("utf-8")] = -0.4
map_max["积极赔偿并取得被害人谅解".decode("utf-8")] = 0
map_min["没有赔偿但取得被害人谅解".decode("utf-8")] = -0.2
map_max["没有赔偿但取得被害人谅解".decode("utf-8")] = 0
map_min["刑事和解".decode("utf-8")] = -0.5
map_max["刑事和解".decode("utf-8")] = 0
map_min["累犯".decode("utf-8")] = -0.4
map_max["累犯".decode("utf-8")] = -0.1
map_min["有前科劣迹".decode("utf-8")] = 0
map_max["有前科劣迹".decode("utf-8")] = 0.1
map_min["被害人为未成年人老人残疾人孕妇等".decode("utf-8")] = 0
map_max["被害人为未成年人老人残疾人孕妇等".decode("utf-8")] = 0.2
map_min["重大灾害疫情期犯罪".decode("utf-8")] = 0
map_max["重大灾害疫情期犯罪".decode("utf-8")] = 0.2

for data in dataInf:
	date = dict(data).get("初始刑期".decode('utf-8'))
	init_date = float(date)
	print "初始刑期: ",init_date
	# ans_min = init_date
	# ans_max = init_date
	reduce_max = 0.0
	reduce_min = -1000.0
	add_max = 0.0
	add_min = 1000.0
	d = dict(data)
	for key in d:
		if key.encode("utf-8") == "初始刑期" or key == "_id":
			continue

		if map_min[key] < 0.0 or map_max[key] < 0.0:
			reduce_max = min(reduce_max , float(d[key]) * map_min[key] * init_date)
			reduce_min = max(reduce_min , float(d[key]) * map_max[key] * init_date)
		else:
			add_max = max(add_max , float(d[key]) * map_max[key] * init_date)
			add_min = min(add_min , float(d[key]) * map_min[key] * init_date)

		# ans_min = min(ans_min , init_date + float(d[key]) * map_min[key] * init_date)
		# ans_max = max(ans_max , init_date + float(d[key]) * map_max[key] * init_date)
	if add_min < 1000.0:
		ans_min = init_date + reduce_max + add_min
	else:
		ans_min = init_date + reduce_max
	if reduce_min > -1000.0:
		ans_max = init_date + reduce_min + add_max
	else:
		ans_max = init_date + add_max
	print "最短刑期: " , ans_min
	print "最长刑期: " , ans_max
	