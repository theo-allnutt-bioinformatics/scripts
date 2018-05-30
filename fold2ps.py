#!/usr/bin/python

import sys
import subprocess as sp


f=sys.argv[1]


outprefix=sys.argv[2]

print "folding"
	
p0=sp.check_output("RNAfold %s --noPS > %s.fold  " %(f,outprefix),shell=True)
	

print "processing fold file to pseudosequence"

r=open(outprefix+".fold",'r')
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
				if seq[t]=="U":
					x="T"
				else:
					x=seq[t]
			if x=="(":
				x="F"
			if x==")":
				x="R"
			pseq=pseq+x
	
		pseqout.write(id+pseq+"\n")
		
		
		
		
		
		
		
		
	