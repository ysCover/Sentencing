# -*- coding: UTF-8 -*-   
import sys
import os
import lxml.etree
import json
import xmltodict
import snownlp
reload(sys) 
sys.setdefaultencoding('utf8')  
import pymysql
import urllib2
import jieba.posseg
import pymongo
import requests

folder = '/home/tc/Desktop/机器学习项目组/project_submit/Sentencing/案件删选/三到七年有期徒刑/'
files = os.listdir(folder)

for file in files: 
	data = {}
	f = open(folder + file)
	text = xmltodict.parse(f.read().encode('utf-8'))
	s = json.loads(json.dumps(text))
	rt = s['writ']['QW']

	# court = rt['WS']['JBFY']['BZFYMC']['@value'].encode('utf-8')
	# Litigant = rt['PJJG']['XSPJJGFZ']['SSCYR']['@value'].encode('utf-8')

	#案件情况描述
	try:
		Situation = rt['AJJBQK']['@value']
	except:
		continue
	reason = ""
	result = ""
	length = len(Situation)
	s1 = s2 = False
	for i in range(length):
		if Situation[i] == '被' and Situation[i+1] == '告' and Situation[i+2] == '人' :
			s1 = True
		if Situation[i] == '，' and (Situation[i+1] == '致' or Situation[i+1] == '造' and Situation[i+2] == '成'):
			s1 = False
		if i > 0 and Situation[i-1] == '，' and (Situation[i] == '致' or Situation[i] == '造' and Situation[i+1] == '成'):
			s2 = True
		if s1 == True:
			reason += Situation[i] 
		if s2 == True:
			result += Situation[i] 
		if Situation[i] == '。':
			break
	# print "reason: " + reason 
	# print "reason: " + result 
	#裁判分析过程(违规行为)

	try:
		CPFXGC = rt['CPFXGC']['@value']
	except:
		continue
	illegal_description = ""
	for i in CPFXGC:
		illegal_description += i
		if i == '。':
			# print illegal_description
			break
	length = len(CPFXGC)
	jjpc = False
	for i in range(length):
		if CPFXGC[i] == '积' and CPFXGC[i+1] == '极' and CPFXGC[i+2] == '赔' and CPFXGC[i+3] == '偿':
			jjpc = True
			break

	wd = jieba.posseg.cut(illegal_description)
	illegal = []
	words = []
	for word,flag in wd:
		# print word
		words.append(word);

	f1 = f2 = f3 = f4 = f5 = f6 = f7 = f8 = f9 = f10 = f11 = False
	ss1 = ss2 = ss3 = 0
	ty = fz = False
	fzlx = ""
	for i in range(0,len(words)):
		# print words[i]
		if f1 == False and (words[i] == ('无证') and words[i+1] == ('驾驶') or words[i] == ('无') and words[i+1] == ('驾驶证') 
		or words[i] == ('无') and words[i+1] == ('机动车') and words[i+2] == ('驾驶证')
		or words[i] == ('驾驶') and words[i+1] == ('资格证')):
			# print "无证驾驶"
			f1 = True
			illegal.append('无证驾驶')
		if f2 == False and (words[i] == ('无') and words[i+1] == ('号牌') 
		or words[i] == ('未') and words[i+1] == ('悬挂') and words[i+2] == ('号牌') 
		or words[i] == ('无') and words[i+1] == ('牌照')):
			# print "驾驶无牌照车辆"
			f2 = True
			illegal.append('驾驶无牌照车辆')
		if f3 == False and (words[i] == '醉酒' or words[i] == '酒后'):
			# print "酒驾"
			f3 = True

			illegal.append('酒驾')
		if f4 == False and words[i] == '超载' :
			# print "超载"
			f4 = True
			illegal.append('超载')
		if f5 == False and words[i] == '超速' :
			# print "超速"
			f5 = True
			illegal.append('超速')		
		if f6 == False and (words[i] == '逆行' or words[i] == '逆向' and words[i+1] == '行驶'):
			# print "逆行"
			f6 = True
			illegal.append('逆行')		
		if f7 == False and words[i] == '追尾' :
			# print "追尾"
			f7 = True
			illegal.append('追尾')
		if f8 == False and words[i] == '闯' and words[i+1] == '红灯' :
			# print "闯红灯"
			f8 = True
			illegal.append('闯红灯')
		if f9 == False and words[i] == '未' and words[i+1] == '确保' and words[i+2] == '安全' :
			# print "危险路段未确保安全"
			f9 = True
			illegal.append('危险路段未确保安全')
		if f10 == False and words[i] == '未' and words[i+1] == '谨慎' and words[i+2] == '驾驶' :
			# print "危险路段未谨慎驾驶"
			f10 = True
			illegal.append('危险路段未谨慎驾驶')
		if f11 == False and (words[i] == '操作' and words[i+1] == '不当' or words[i] == '操作' and words[i+1] == '规范'):
			# print "驾驶操作不当,未按照操作规范安全驾驶"
			f11 = True
			illegal.append('驾驶操作不当')
		if words[i] == '死亡':
			j = i-1
			while words[j] != '，':
				if words[j] == '一':
					ss1 = 1
					break
				elif words[j] == '二' :
					ss1 = 2
					break
				elif words[j] == '两' :
					ss1 = 2
					break
				elif words[j] == '三':
					ss1 = 3
					break
				elif words[j] == '四':
					ss1 = 4
					break
				elif words[j] == '五':
					ss1 = 5
					break
				elif words[j] == '六':
					ss1 = 6
					break
				elif words[j] == '七':
					ss1 = 7
					break
				elif words[j] == '八':
					ss1 = 8
					break
				elif words[j] == '九':
					ss1 = 9
					break
				elif words[j] == '十':
					ss1 = 10
					break
				elif words[j] == '多':
					ss1 = -1
					break
				j -= 1
		if words[i] == '受伤' or words[i] == '重伤':
			j = i-1
			while words[j] != '，':
				if words[j] == '一':
					ss2 = 1
					break
				elif words[j] == '二' :
					ss2 = 2
					break
				elif words[j] == '两' :
					ss2 = 2
					break
				elif words[j] == '三':
					ss2 = 3
					break
				elif words[j] == '四':
					ss2 = 4
					break
				elif words[j] == '五':
					ss2 = 5
					break
				elif words[j] == '六':
					ss2 = 6
					break
				elif words[j] == '七':
					ss2 = 7
					break
				elif words[j] == '八':
					ss2 = 8
					break
				elif words[j] == '九':
					ss2 = 9
					break
				elif words[j] == '十':
					ss2 = 10
					break
				elif words[j] == '多':
					ss2 = -1
					break
				j -= 1
		if words[i] == '轻伤':
			j = i-1
			while words[j] != '，':
				if words[j] == '一':
					ss3 = 1
					break
				elif words[j] == '二' :
					ss3 = 2
					break
				elif words[j] == '两' :
					ss3 = 2
					break
				elif words[j] == '三':
					ss3 = 3
					break
				elif words[j] == '四':
					ss3 = 4
					break
				elif words[j] == '五':
					ss3 = 5
					break
				elif words[j] == '六':
					ss3 = 6
					break
				elif words[j] == '七':
					ss3 = 7
					break
				elif words[j] == '八':
					ss3 = 8
					break
				elif words[j] == '九':
					ss3 = 9
					break
				elif words[j] == '十':
					ss3 = 10
					break
				elif words[j] == '多':
					ss3 = -1
					break
				j -= 1
		if ty == False and words[i] == '逃逸' :
			ty = True
		if fz == False and (words[i] == '全部' or words[i] == '主要' or words[i] =='次要')and words[i+1] == '责任' :
			fz = True
			fzlx = words[i]

	for word,flag in wd:	
		if word.find('车') != -1 and flag == 'n':
			car = word
			break
	
# 获取的案件信息都不涉及少年法庭
# 14岁到16岁之间犯罪 
	# print "是否14岁到16岁之间犯罪: 否"
	data['是否14岁到16岁之间犯罪'] = "否"
# 16岁到18岁之间犯罪 
	# print "是否16岁到18岁之间犯罪: 否"
	data['是否16岁到18岁之间犯罪'] = "否"
# 事发原因
	# print "事发原因: " + reason 
	data['事发原因'] = reason
# 财产损失 
	# print "财产损失: " + result 
	data['财产损失'] = result
# 违规行为
	item = []
	# print "违规情况: ", 
	for i in range(0,len(illegal)):
		item.append(illegal[i])
		# print illegal[i] ,
	data['违规情况'] = item
# 负何种责任
	# print "\n负何种责任: " + fzlx
	data['负何种责任'] = fzlx

# 死亡人数 
	if ss1 == -1:
		# print "死亡人数: 多人"
		data['死亡人数'] = "多人"
	else:
		# print "死亡人数: ",ss1
		data['死亡人数'] = ss1
# 重伤人数 
	if ss2 == -1:
		# print "重伤人数: 多人"
		data['重伤人数'] = "多人"
	else:
		# print "重伤人数: ",ss2
		data['重伤人数'] = ss2
# 轻伤人数 
	if ss3 == -1:
		# print "轻伤人数: 多人"
		data['轻伤人数'] = "多人"
	else:
		# print "轻伤人数: ",ss3
		data['轻伤人数'] = ss3

#量刑情节
	# Sentencing = rt['CPFXGC']['LXQJ']
	# try:
	# 	print "量刑情节: 		" + Sentencing['FDLXQJ']['QJ']['@value']
	# except:
	# 	print ""
	# try:
	# 	print "法定量刑情节类别:   " + Sentencing['FDLXQJ']['LXQJLB']['@value']	
	# except:
		# print ""
	s1 = s2 = s3 = s4 = s5 = s6 =False
	try:
		Sentencing = rt['CPFXGC']['LXQJ']['ZDLXQJ']
		# print "被告人是否同意认罪程序:   " + rt['CPFXGC']['BGRTYRZCX']['@value']
		n = len(Sentencing)
		for i in range(0,n):
			# print "认罪态度:       " + Sentencing[i]['QJ']['@value'] 
			if Sentencing[i]['QJ']['@value'] == "自首":
				s1 = True
			elif Sentencing[i]['QJ']['@value'] == "犯罪后采取补救措施降低损失":
				s2 = True
			elif Sentencing[i]['QJ']['@value'] == "主动取得被害人谅解":
				s3 = True
			elif Sentencing[i]['QJ']['@value'] == "认罪态度好":
				s4 = True
			elif Sentencing[i]['QJ']['@value'] == "老年人、智障人、残疾人犯罪":
				s5 = True
			elif Sentencing[i]['QJ']['@value'] == "手段恶劣，动机卑劣":
				s6 = True
	except:
		print ""
# 是否有前科劣迹
	qklj = "没有" 
	try:
		if rt['DSR']['YSF']['QKLJ'][0]['@nameCN'] == '前科劣迹' or rt['DSR']['YSF']['QKLJ']['@nameCN'] == '前科劣迹':
			qklj = "有" 
			# print "是否有前科劣迹: 有"
		# else:
			# print "是否有前科劣迹: 没有"
	except:
		qklj = "没有" 
		# print "是否有前科劣迹: 没有"
	data['是否有前科劣迹'] = qklj
# 是否逃逸
	if ty == True:
		# print "是否逃逸: 是"
		data['是否逃逸'] = "是"
	else:
		# print "是否逃逸: 否"
		data['是否逃逸'] = "否"
# 是否自首
	if s1 == True:
		# print "是否自首: 是"
		data['是否自首'] = "是"
	else:
		# print "是否自首: 否"
		data['是否自首'] = "否"
# 是否积极赔偿
	if jjpc == True:
		# print "是否积极赔偿: 是"
		data['是否积极赔偿'] = "是"
	else:
		# print "是否积极赔偿: 否"
		data['是否积极赔偿'] = "否"
# 犯罪后是否采取补救措施
	if s2 == True:
		# print "犯罪后是否采取补救措施: 是"
		data['犯罪后是否采取补救措施'] = "是"
	else:
		# print "犯罪后是否采取补救措施: 否"
		data['犯罪后是否采取补救措施'] = "否"
# 主动取得被害人谅解
	if s3 == True:
		# print "是否达成和解: 是"
		data['是否达成和解'] = "是"
	else:
		# print "是否达成和解: 否"
		data['是否达成和解'] = "否"
# 认罪态度
	jbzz = False
	if rt['CPFXGC']['BGRTYRZCX']['@value'] == '否':
		jbzz = True
	if jbzz == True:
		# print "认罪态度: 拒不认罪"
		data['认罪态度'] = "拒不认罪"
	elif s4 == True:
		# print "认罪态度: 良好"
		data['认罪态度'] = "良好"
	else:
		# print "认罪态度: 一般"
		data['认罪态度'] = "一般"
# 罪犯类型是否老年人、智障人、残疾人
	if s4 == True:
		# print "罪犯类型是否老年人、智障人、残疾人: 是"
		data['罪犯类型是否老年人、智障人、残疾人'] = "是"
	else:
		# print "罪犯类型是否老年人、智障人、残疾人: 否"
		data['罪犯类型是否老年人、智障人、残疾人'] = "否"

# 是否手段恶劣，动机卑劣
	if s6 == True:
		# print "是否手段恶劣，动机卑劣: 是"
		data['是否手段恶劣，动机卑劣'] = "是"
	else:
		# print "是否手段恶劣，动机卑劣: 否"
		data['是否手段恶劣，动机卑劣'] = "否"


#判决结果
	Result = rt['PJJG']['XSPJJGFZ']['BSPJJG']['ZXPF']
	zxxq = "null"
	hxxq = "null"
	try:
		zxxq = Result['HX']['HXXQ']['@value']
		# print "缓刑刑期:   " + Result['HX']['HXXQ']['@value']
	except:
		zxxq = "null"
		# print "缓刑刑期:   null "
	try:
		hxxq = Result['ZX']['ZXXQ']['@value']
		# print "主刑刑期:   " + Result['ZX']['ZXXQ']['@value']
	except:
		hxxq = "null"
		# print "主刑刑期:   null "
	data['主刑刑期'] = zxxq
	data['缓刑刑期'] = hxxq
	# print data

#法条
	ftitem = []
	# print "\n法条: "
	try:
		rt = s['writ']['QW']['CPFXGC']['CUS_FLFT_FZ_RY']['CUS_FLFT_RY']
		nums = len(rt)
		flag = True
		for x in rt:
			if x == '@nameCN':
				flag = False
			else:
				break
		if flag == False:
			print "\n"
		else: 
			a = [0 for x in range(0, nums)]
			for i in range(0,nums):
				a[i] = rt[i]['@value'].encode('utf-8')
				ftitem.append(a[i])
				
		data['法条'] = ftitem
	except:
		data['法条'] = []
	client =  pymongo.MongoClient('localhost',27017)
	db = client['Sentencing']
	collection = db['factor3_7']
	collection = collection.insert(data)
	f.close()

