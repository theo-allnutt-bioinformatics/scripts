#!/usr/bin/env python3

from Bio import SeqIO
import sys


f = open(sys.argv[1],'r') #gff3
h=open(sys.argv[2],'r')#ref genome

g= open(sys.argv[3],'w') #multifasta out


record = SeqIO.to_dict(SeqIO.parse(h, 'fasta'))

for i in f:

	k=i.rstrip("\n").split("\t")
	
	contigname=k[0]
	
	numptname=k[-1].split("ID=")[1].rstrip("\n")
	
	start=int(k[3])-1
	
	end=int(k[4])-1
	
	print(contigname,numptname)
	
	g.write(">%s\n%s\n" %(numptname,str(record[contigname].seq[start:end])))
	
	
	


