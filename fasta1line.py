#!/usr/bin/env python

import sys

#make fastas into single line sequence


f=open(sys.argv[1],'r')
g=open(sys.argv[2],'w')

c=0
k=[]
x=f.readline()
while x:
	c=c+1
	
	k.append(x)
	
	if c>1:
		if k[-2][0]==">":
			g.write(k[-2])
		if k[-2][0]<>">" and k[-1][0]<>">":
			g.write(k[-2].rstrip("\n"))
		if k[-2][0]<>">" and k[-1][0]==">":
			g.write(k[-2])
	x=f.readline()

if k[-1]<>"\n":
	g.write(k[-1])
	