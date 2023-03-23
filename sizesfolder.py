#!/usr/bin/env python3

from Bio import SeqIO
import sys
import os
import re
import glob


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

folder = sys.argv[1] #working folder
				  
filelist=glob.glob(folder+"/*" )

filelist.sort(key=tokenize)

print(filelist)

for i in filelist:			  
	f=open(i,'r')
	
	for x in SeqIO.parse(f,sys.argv[2]):

		print(x.id+"\t"+i.split("/")[-1]+"\t"+str(len(x.seq)))
	