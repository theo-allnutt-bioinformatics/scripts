#!/usr/bin/python

#from Bio import SeqIO
import sys

listfile1 = open(sys.argv[1],'r') 

inputfile = open(sys.argv[2],'r') 

ucfile = open(sys.argv[3],'r')

outfolder=sys.argv[4]

limitn=int(sys.argv[5])

print 'Reading sequence file'
#x = SeqIO.to_dict(SeqIO.parse(inputfile,'fasta')) # key_function = lambda rec : rec.description.split(";")[0]

x = {}

for i in inputfile:
	if i[0]==">":
		id=i[1:].split(";")[0].rstrip("\n")
		x[id]=""
	else:
		x[id]=x[id]+i.rstrip("\n")

c=0

print 'Fetching sequences from listed clusters'

for i in listfile1:
		
	#get clusters and seqs
		
	id1 = i.rstrip("\n") #cluster name to get
	
	ucfile.seek(0)
	
	for clus1 in ucfile:
		
		k=clus1.split("\t")
		name =k[8].split(";")[0].rstrip("\n")
		name2 =k[9].split(";")[0].rstrip("\n")
		
		if k[0]=="C" and name==id1:
			print "Fetching cluster", id1
			g=open(outfolder+"/"+id1+".fasta",'w')
			print c
			c=0
		
		if k[0]=="H" and name2==id1 and c<limitn:
			c=c+1
			id2=k[8].rstrip("\n").split(";")[0]
			g.write(">"+id2+"\n"+x[id2]+"\n")
			
		

	
		









	

		






