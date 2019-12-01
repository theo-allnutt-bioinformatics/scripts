#!/usr/bin/env python

#Theo Allnutt 2019 for 082
# compare ranks of items and get other stats
#http://codalism.com/research/papers/wmz10_tois.pdf
#https://github.com/ragrawal/measures/blob/master/measures/rankedlist/RBO.py

#list_compare.py estimates_file expected_file 

import sys
import scipy.stats as sp
import re
import glob
import os

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

folder= sys.argv[1]

expected_folder=sys.argv[2] #expected files must have the same number as the test file

g=open(sys.argv[3],'w')

name2=sys.argv[3].split(".")[0]

g.write("name\texp_n\tn\trbo\textra\tmissing\tR\tp\n")

filelist=glob.glob(folder)
filelist.sort(key=tokenize)

expfilelist=glob.glob(expected_folder)
expfilelist.sort(key=tokenize)

print filelist
print expfilelist

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


for x,y in zip(filelist,expfilelist):

	f=open(x,'r')
	e=open(y,'r')
	
	print x,y
	
	name1=x.split("/")[-2]+"_"+x.split("/")[-1].split(".")[0]
	
	list1=[]
	list2=[]
	count1={}
	count2={}
	for i in f:

		k = i.rstrip("\n").split("\t")
		
		list1.append(k[0])
		count1[k[0]]=int(k[1])
		
	for i in e:

		k = i.rstrip("\n").split("\t")
			
		list2.append(k[0])
		count2[k[0]]=int(k[1])
		
	rbo=RBO(list1,list2, p = 0.98)

	extra=0
	missing=0
	p1=[]
	p2=[]

	for x in list2:
		if x not in list1:
			extra=extra+1
	for x in list1:
		if x not in list2:
			missing=missing+1

	for x in list1:
		if x in count2.keys():
			p1.append(count1[x])
			p2.append(count2[x])


	rho, pval = sp.pearsonr(p1,p2)

	output= str(len(list1))+"\t"+str(len(list2))+"\t"+str(rbo)+"\t"+str(extra)+"\t"+str(missing)+"\t"+str(rho)+"\t"+str(pval)

	g.write(name2+"\t"+output+"\n")

	









