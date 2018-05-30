#!/usr/bin/python
import sys
import re
import glob
import subprocess
from Bio import SeqIO


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))



folder = sys.argv[1] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

outfolder=sys.argv[2]

for i in filelist:

	name=i.split("/")[-1]
	g=open(outfolder+"/"+"contig1_"+name,'w')
	j=open(i,'r')
	
	for x in SeqIO.parse(j,'fasta'):
	
		
		SeqIO.write(x,g,'fasta')
		
		break
