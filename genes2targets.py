#!/usr/bin/env python3

from Bio import SeqIO
import sys
import os
import re
import glob
import concurrent.futures

#r10.11


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))



def maketargets(i):

	print(i)

	f=open(i,'r')

	gene=i.split("/")[-1].split(".")[0]
	
	c2=0
	
	for x in SeqIO.parse(f,'fasta'):
			
		species="_".join(str(p) for p in x.id.split("_")[:-1])
		
		species=species.replace(".","")
		
		name=f"{species}-{gene}"
		
		if name in names: #rename if duplicated
			c2=c2+1
			print(name,"duplicated, renaming",f"{species}_{c2}-{gene}")
			
			name=f"{species}_{c2}-{gene}"
			names.append(name)
			
		else:
			names.append(name)
			c2=0
		
		
		g.write(f">{name}\n{str(x.seq)}\n")

	
#global

filelist=glob.glob(sys.argv[1])

filelist.sort(key=tokenize)

outfile=sys.argv[2]


g=open(outfile,'w')		  

names=[]

print("files to process:",filelist)

if __name__ == '__main__':
	
	for i in filelist:
	
		maketargets(i)
		