#!/usr/bin/python

#makes pseudo DNA sequence from structure - does not retain dot . bases as fold2ps.py does

import sys
import subprocess as sp


f=sys.argv[1]


outprefix=sys.argv[2]

g=open(sys.argv[3],'w')

print "folding"
	
p0=sp.check_output("RNAfold %s --noPS > %s  " %(f,outprefix),shell=True)
	

print "processing fold file to pseudosequence"

r=open(outprefix,'r')
c=0

for i in r:
	c=c+1
	if c==1:
		id=i
	if c==2:
		seq=i
	if c==3:
		fold=i
		c=0
		pseq=""
		t=-1
		for x in fold:
			t=t+1
			if x==" ":
				break
			if x==".":
				x="A"
				
			if x=="(":
				x="G"
			if x==")":
				x="C"
			pseq=pseq+x
	
		g.write(id+pseq+"\n")
		
		
		
		
		
		
		
		
	