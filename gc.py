#!/usr/bin/python

from Bio import SeqIO
import sys


f=open(sys.argv[1],'r')

fmt=sys.argv[2]

for i in SeqIO.parse(f,fmt):

	seq1=str(i.seq)
	len1=float(len(i.seq))
	
	cg1=float(seq1.count("g")+seq1.count("c")+seq1.count("G")+seq1.count("C"))
	
	pc1=float((cg1/len1)*100)
	
	print str(i.id), pc1