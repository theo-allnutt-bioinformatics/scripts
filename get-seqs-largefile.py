#!/usr/bin/env python3

import sys


def getfasta():
	cnt=0
	tot=len(seqlist)
	seqtot=0
	
	n=0
	for x in f:
	
		if n==1:
			if x[0]!=">":
				g.write(x)
				
			else:
				n=0
			
		if x[0]==">" and n==0:
			seqtot=seqtot+1
			id1=x[1:].rstrip("\n").split(" ")[0]
			
			if id1 in seqlist:
				n=1
				g.write(x)
				cnt=cnt+1
				print('Found',cnt,'of',tot,'in list',end='\r')
		
def getfastq():
	cnt=0
	tot=len(seqlist)
	seqtot=0
	header=f.readline()[:4]
	f.seek(0)
	n=0
	
	for x in f:
	
		if n==1:
			if x[0]!="+":
				g.write(x)
				
			else:
				n=2
				
		if n==2:
			if x[:4]!=header:
				g.write(x)
				
			else:
				n=0
			
		if x[:4]==header and n==0:
			seqtot=seqtot+1
			
			id1=x[1:].rstrip("\n").split(" ")[0]
			
			if id1 in seqlist:
				n=1 #1=write seq
				g.write(x)
				cnt=cnt+1
				print('Found',cnt,'of',tot,'in list',end='\r')
				if cnt==sample:
					break
	
					

#global

listfile1 = open(sys.argv[1],'r')
seqlist=[]
for x in listfile1:
	seqlist.append(x.rstrip("\n"))
listfile1.close()

f = open(sys.argv[2],'r') 

g = open(sys.argv[3],'w') 

sample=int(sys.argv[4])

cnt=0
tot=len(seqlist)
seqtot=0


		
if sys.argv[2][-1]=="a":

	getfasta()
	
if sys.argv[2][-1]=="q":

	getfastq()

print()

g.close()

