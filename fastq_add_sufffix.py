#!/usr/bin/env python3

import sys


def fixsuffix(f,g,s):

	print("seq2dict")

	data={}

	i=f.readline()
	while i!="":
		
		id1=i.rstrip("\n").split(" ")[0]
		
		s1=f.readline()#seq
		i=f.readline() #+
		q1=f.readline() #qual
		i=f.readline() #next id
	
		g.write(id1+s+"\n"+s1+"+\n"+q1)
		
	
	
	
	
#global

f=open(sys.argv[1],'r')
g=open(sys.argv[2],'w')
s=sys.argv[3]

fixsuffix(f,g,s)