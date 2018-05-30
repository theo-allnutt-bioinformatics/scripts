#!/usr/bin/python

#from Bio import SeqIO
import sys
from Bio import SeqIO

listfile1 = open(sys.argv[1],'r') 

inputfile = open(sys.argv[2],'r') 

g = open(sys.argv[3],'w') 

delim=sys.argv[4]

print 'reading file'
x = SeqIO.to_dict(SeqIO.parse(inputfile,'fasta'))

print x.keys()

'''
x = {}
for i in inputfile:
	if i[0]==">":
		id=i.split(">")[1].split(delim).rstrip("\n")
		x[id]=""
	else:
		x[id]=x[id]+i.rstrip("\n")
'''

c=0
f=0
print 'fetching sequences'
for k in listfile1:

	name=k.split("\t")[0]
	orient= k.split("\t")[1].rstrip("\n")
	print name, orient,
	
	if name in x.keys() and orient=="f":
		
		g.write(">"+name+"\n"+str(x[name].seq)+"\n")
		print "written"
			
	if name in x.keys() and orient=="r":
		
		g.write(">"+name+"\n"+str(x[name].reverse_complement().seq)+"\n")
		print "written"

	if name not in x.keys():
		print "not found"
		
		
	
	











	

		






