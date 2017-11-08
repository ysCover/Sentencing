# -*- coding: UTF-8 -*-
import os
import json
import lxml.etree
import xmltodict
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

folder_read = "/home/tc/Desktop/机器学习项目组/trafficdata/"      #自己文件的路径
folder_write = "/home/tc/Desktop/机器学习项目组/三到七年有期徒刑/"  #自己文件的路径
files = os.listdir(folder_read)
for file in files:
	fr = open(folder_read + file)
	text = xmltodict.parse(fr.read().encode('utf-8'))
	s = json.loads(json.dumps(text))
	flag = False
	try:
		Result = s['writ']['QW']['PJJG']['XSPJJGFZ']['BSPJJG']['ZXPF']['ZX']['ZXXQ']['@value']
		if Result[1] == "年" and (Result[0] == "三" or Result[0] == "四" or Result[0] == "五" or Result[0] == "六" or Result[0] == "七" and len(Result) == 2 ):
			flag = True
	except:
		continue

	if flag == True:
		shutil.copyfile(folder_read + file,folder_write + file)



