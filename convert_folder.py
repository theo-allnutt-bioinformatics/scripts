#!/usr/bin/python
from Bio import SeqIO
import sys
import os
import re
import glob
import sys
import subprocess as sp

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#get details on all seqs in a folder (with specified extension_

folder = sys.argv[1] #working folder

outfolder=sys.argv[2]

fmt = sys.argv[3]

outfmt = str(sys.argv[4])

if fmt=="fa" or fmt=="fna":
	fmt="fasta"
if fmt=="fq":
	fmt="fastq"
if fmt=="gbk":
	fmt="genbank"

print 'in format:', fmt, 'out format', outfmt

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

#Theo Allnutt 2016
#Converts files of different sequence format
#usage: convert.py infile informat outformat [see http://biopython.org/wiki/SeqIO] 


for i in filelist:
	'''
	f = open(i,'rb')
	outputfile = outfolder+"/"+i.split("/")[-1].split(".")[0] + "."+outfmt
	g = open(outputfile,'w')

	count = SeqIO.convert(f, fmt,g, outfmt)

	print("Converted %i records" % count)
'''

	










