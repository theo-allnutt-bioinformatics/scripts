#!/usr/bin/env python3

from Bio import SeqIO
import sys
import os
import subprocess

#convert genbank to multi fasta nucleotide format

inputfile = sys.argv[1] 
outfile = sys.argv[2]

f = open(inputfile,'r')

g= open(outfile,'w')


for seq_record in SeqIO.parse(f, "genbank") :
	print("Dealing with GenBank record %s" % seq_record.id)
	c=0
	c2=0
	
	for seq_feature in seq_record.features :
		
		#print seq_feature.qualifiers.keys()
		if seq_feature.type=="CDS" :
			#get location
			if 'translation' in seq_feature.qualifiers.keys():# and 'gene' in seq_feature.qualifiers.keys():
				try:
					startpos=int(str(seq_feature.location).split("(")[0].lstrip("[").rstrip("]").split(":")[0])
					endpos=int(str(seq_feature.location).split("(")[0].lstrip("[").rstrip("]").split(":")[1])
					print("CDS",startpos,endpos)
				except:
					c2=c2+1
					print("translation failed")
					
				c=c+1
				g.write(">"+seq_record.id+"-"+str(c))
				if 'locus_tag' in seq_feature.qualifiers.keys():
					g.write(" "+seq_feature.qualifiers['locus_tag'][0])
				if 'gene' in seq_feature.qualifiers.keys():
					g.write(" "+seq_feature.qualifiers['gene'][0])
				if 'product' in seq_feature.qualifiers.keys():
					g.write(" "+seq_feature.qualifiers['product'][0])
		
				g.write("\n"+seq_feature.qualifiers['translation'][0]+"\n")
				'''
				try:
					g.write(" "+seq_feature.qualifiers[locus_tag][0],
							seq_feature.qualifiers['gene'][0],
							seq_feature.qualifiers['product'][0],
							seq_feature.qualifiers['translation'][0])
							#seq_record.seq[startpos:endpos]))
				except:
					print "failed parse"
					p2=p2=1
				'''
				
	print(str(seq_record.id), "genes", c,"translation failed", c2)
	
