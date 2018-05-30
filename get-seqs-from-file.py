#!/usr/bin/python

#from Bio import SeqIO
import sys

listfile1 = open(sys.argv[1],'r') 

inputfile = open(sys.argv[2],'r') 

g = open(sys.argv[3],'w') 

delim=sys.argv[4]

print 'reading file'
#x = SeqIO.to_dict(SeqIO.parse(inputfile,'fasta'))

x = {}

for i in inputfile:

	if i[0]==">":
	
		id=i.split(">")[1].rstrip("\n")
		x[id]=""
	else:
		x[id]=x[id]+i.rstrip("\n")

#print x

data={}
genes=[]
print 'parsing file'
for i in x.keys():
	#print x[i].description.split(",")[0]
	if delim<>"":
		data[i.split(delim)[0]]=x[i]
	else:
		data[i]=x[i]
	
print len(data.keys()),'sequences'

c=0
f=0
print 'fetching sequences'
for k in listfile1:
		name=k.rstrip("\n")#.split(delim)[0]
		try:
			c=c+1
		
			g.write(">"+str(name)+"\n"+str(data[name])+"\n")
		except:
			c=c-1
			print name,'not found'



print "got %d sequences" %c








	

		






