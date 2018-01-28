#-*- coding:utf-8 -*-
import lxml.etree
import xmltodict
import sys
reload(sys) 
sys.setdefaultencoding('utf8') 
import json
import jieba
import os
import re
import jieba.posseg as jbpos

Key_wd1 = ['恰逢','遇','突遇','恰遇','对','因','时因','由于','于是','遂','在','未','未尽','未能']
Key_wd2 = ['时','处','中','后','下']
Key_wd3 = ['掉头','逆时针','逆向','占','占道','占用','起步','超速','超速行驶','超载','变道','转向','转弯','追尾','超车','超越','会车','变道','刹车','制动','停车','停放','倒车','顺行','驶入','驶出','穿过','右拐','左拐','左转','右转','左转弯','右转弯','靠右','靠左','试图','临近','发现','观察','察看','瞭望','掺望','避让','躲避','判断','采取','操作','坠入','掉入','落入','翻入','降低','追','避让','摔倒','翻滚','翻覆','侧翻','仰翻','侧滑','滑行','刮擦','跌落','倒地','停','停于','压','塌','压塌'] 
Key_wd4 = ['安全','文明','规范','规定','限速','原则','合格','设施','标准','核定','技术标准','隐患','安全隐患','交通信号','指示灯','指示','标志','标线','情况']
Key_wd5 = ['不周','不够','不慎','不当','不力','不足','不及','不良','忽视','疏于','疏忽','大意','麻痹','忽视','疏忽大意','未谨慎','未察明','妨碍','违法','违章','违反','违反规定','闯红灯','超过','失误','失控','失效','报废','故障','越线','炫目','模糊','及时','确保','确认','遵守','保持','按照','谨慎','检验','注意','符合','临危','疲劳','打瞌睡','状态','醉酒','故障','按规定','采取措施','观察不周','躲闪不及','确保安全','估计不足','采取有效','操作失误','减速慢行','紧急制动','及时发现','逆向行驶']
Key_wd6 = ['施工','狭窄','冰雪','大雾','雨天','潮湿','淤泥','积水','路面','湿滑','夜间','视线','能见度','破损']

Dict1 = {}
Dict2 = {}
Dict3 = {}
Dict4 = {}
Dict5 = {}
Dict6 = {}

for key in Key_wd1:
	Dict1[key] = 'Start'
for key in Key_wd2:
	Dict2[key] = 'End'
for key in Key_wd3:
	Dict3[key] = 'Drive'
for key in Key_wd4:
	Dict4[key] = 'Rule'
for key in Key_wd5:
	Dict5[key] = 'Status'
for key in Key_wd6:
	Dict6[key] = 'Ement'

# folder = '/Users/siming/Desktop/我的CRF/事发原因抽取CRF/data/'
# files = os.listdir(folder)

rfile = open('/Users/siming/Desktop/我的CRF/事发原因抽取CRF/rigth','r')
line = rfile.readline()

testfile = open('train_start_end','w')

wd_st = False
while line:
	if line == '\n':
		wd_st = False 
		testfile.write('\n');
		line = rfile.readline()
		continue

	ln = line.split()
	wd = ln[0].encode('utf-8')
				# 关键词标记
	key_type = 'N'
	# print wd
	try:
		if wd in Dict1:
			key_type = 'Start'
		elif wd in Dict2:
			key_type = 'End'
		elif wd in Dict3:
			key_type = 'Drive'
		elif wd in Dict4:
			key_type = 'Rule'
		elif wd in Dict5:
			key_type = 'Status'
		elif wd in Dict6:
			key_type = 'Ement'
	except:
			key_type = 'N'

	if wd_st == False and key_type == 'Start':
		print "tes"
		wd_st = True
		testfile.write(wd.encode('utf-8') + '\t' + 'B' + '\n')
	elif wd_st == True :
		if key_type == 'End':
			testfile.write(wd.encode('utf-8') + '\t' + 'E' + '\n')
			wd_st = False
		else:
			testfile.write(wd.encode('utf-8') +  '\t' + 'M' + '\n')
	else:
		testfile.write(wd.encode('utf-8') +  '\t' + 'N' + '\n')

	line = rfile.readline()

rfile.close()
testfile.close()
