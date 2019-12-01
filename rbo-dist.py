#!/usr/bin/env python


#Theo Allnutt 2016
# compare ranks of items
#http://codalism.com/research/papers/wmz10_tois.pdf
#https://github.com/ragrawal/measures/blob/master/measures/rankedlist/RBO.py

import sys
import os
import re
import glob

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
folder = sys.argv[1] #working folder

g= open(sys.argv[2],'w')

num=int(sys.argv[3])

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

print filelist


def RBO(l1, l2, p = 0.98):
	"""
		Calculates Ranked Biased Overlap (RBO) score. 
		l1 -- Ranked List 1
		l2 -- Ranked List 2
	"""
	if l1 == None: l1 = []
	if l2 == None: l2 = []
	
	sl,ll = sorted([(len(l1), l1),(len(l2),l2)])
	s, S = sl
	l, L = ll
	if s == 0: return 0

	# Calculate the overlaps at ranks 1 through l 
	# (the longer of the two lists)
	ss = set([]) # contains elements from the smaller list till depth i
	ls = set([]) # contains elements from the longer list till depth i
	x_d = {0: 0}
	sum1 = 0.0
	for i in range(l):
		x = L[i]
		y = S[i] if i < s else None
		d = i + 1
		
		# if two elements are same then 
		# we don't need to add to either of the set
		if x == y: 
			x_d[d] = x_d[d-1] + 1.0
		# else add items to respective list
		# and calculate overlap
		else: 
			ls.add(x) 
			if y != None: ss.add(y)
			x_d[d] = x_d[d-1] + (1.0 if x in ss else 0.0) + (1.0 if y in ls else 0.0)	 
		#calculate average overlap
		sum1 += x_d[d]/d * pow(p, d)
		
	sum2 = 0.0
	for i in range(l-s):
		d = s+i+1
		sum2 += x_d[d]*(d-s)/(d*s)*pow(p,d)

	sum3 = ((x_d[l]-x_d[s])/l+x_d[s]/s)*pow(p,l)

	# Equation 32
	rbo_ext = (1-p)/p*(sum1+sum2)+sum3
	return rbo_ext
	


filelist2=filelist

g.write(str(len(filelist))+"\n")

for i in filelist:
	print i
	name1=i.split("/")[1].split(".")[0]
	if len(name1)>=9:
		name1=name1[:9]+" "
	else:
		name1=name1+" "*(10-len(name1))
	
	f = open(i,'r')
	list1=[]
	f.readline()
	for x in f:
		k = x.rstrip("\n").split("\t")
		list1.append(k[0])
	
	g.write(name1)
	
	for j in filelist2:
		
		f2=open(j,'r')
		list2=[]
		f2.readline()
		for y in f2:
			k = y.rstrip("\n").split("\t")
	
			list2.append(k[0])
			
		rbo = 1-RBO(list1[:num],list2[:num], p = 0.98)
		if rbo < 1E-7:
			rbo=0
		
		g.write(str(rbo)+" ")
		
	g.write("\n")
	
	











