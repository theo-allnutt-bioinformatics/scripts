#!/usr/bin/env python3

from Bio import SeqIO
import sys
import random

f = open(sys.argv[1],'r') #gff3
h=open(sys.argv[2],'r')#ref genome

blen=int(sys.argv[3])

g= open(sys.argv[4],'w') #multifasta out

randfile=open("random.fasta",'w')

record = SeqIO.to_dict(SeqIO.parse(h, 'fasta'))
c=0
for i in f:

	k=i.rstrip("\n").split("\t")
	
	contigname=k[0]
	
	numptname=k[-1].split("ID=")[1].rstrip("\n")
	
	ori=k[6]
	
	x=int(k[3])
	y=int(k[4])
	
	if ori=="+":
		
		seq1=record[contigname].seq[x-blen:x]
		#print(f">{numptname} {contigname}\n{seq1}\n")
		g.write(f">{numptname} {contigname}\n{seq1}\n")
		
	if ori=="-":
		
		seq1=record[contigname].seq[y:y+blen].reverse_complement()
		
		#print(f">{numptname} {contigname}\n{seq1}\n")
		g.write(f">{numptname} {contigname}\n{seq1}\n")
	
	
	#random
	len1=len(record[contigname].seq)-blen
	r1=random.randrange(0,len1)
	c=c+1
	randfile.write(f">{c}\n{str(record[contigname].seq[r1:r1+blen])}\n")


