#!/usr/bin/env python


import sys

f = open(sys.argv[1],'r')

data={}
samples=[]
z=[]

for i in f:
	z.append(i)

s = len(z)
c=-1
while c< s-1:

	c=c+1
	
	if z[c][0]=="+": #skip quality scores in fastq to avoid @
		c=c+1
	
	#print z[c]
	
	if z[c][0]==">" or z[c][0]=="@":
	
		k=z[c][1:].split(".")[0]
		
		if k not in data.keys():
		
			samples.append(k)
			
			data[k]=1
			
		else:
		
			data[k]=data[k]+1

samples.sort()
			
for i in samples:

	print i,data[i]
			