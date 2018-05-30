#!/usr/bin/python

from Bio import SeqIO
import sys

listfile1 = open(sys.argv[1],'r') 

inputfile = open(sys.argv[2],'r') 

g = open(sys.argv[3],'w') 



donotget=[]
for i in listfile1:
	donotget.append(i.rstrip("\n"))
c=0
for x in SeqIO.parse(inputfile,'fasta'):
	if x.id not in donotget:
		c=c+1
		g.write(">"+str(x.id)+"\n"+str(x.seq)+"\n")



print "got %d sequences" %c








	

		






