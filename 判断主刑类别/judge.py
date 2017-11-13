# -*- coding:utf-8 -*-

x1 = input()
x2 = input()
x3 = input()
x4 = input()
x5 = input()
x6 = input()
x7 = input()
x8 = input()
x9 = input()
x10 = input()

y = 0
if x8 == 1:
	y = 2
elif x6 == 1 or (x1 >= 5 or x2 >= 2 and x9 == 1 ) or (x2 >= 6 and x10 == 1) or (x3 == 1 and x9 == 1 or x5 >= 600000):
	y = 1
elif x7 == 1 and (x1 > 0 or x2 > 0 or x3 ==1):
	y = 0 

print "ans: ", y 
	