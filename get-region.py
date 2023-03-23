#!/usr/bin/env python3


import sys
from Bio import SeqIO

f = open(sys.argv[1],'r') #fasta file
contig=sys.argv[2]
range1=sys.argv[3]
st=int(range1.split("-")[0])
en=int(range1.split("-")[1])


for i in SeqIO.parse(f,'fasta'):

	if i.id==contig:
	
		print(">"+contig+"\n"+i.seq[st:en]+"\n")
		
