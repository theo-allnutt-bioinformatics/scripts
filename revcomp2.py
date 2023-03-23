#!/usr/bin/env python3
import sys
import re
import glob
from Bio import SeqIO


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))



folder = sys.argv[1] # input folderd

outfolder = sys.argv[2] #output folder


filelist=glob.glob(folder)

filelist.sort(key=tokenize)
#print filelist
samples=[]
data={}

for i in filelist:
	name = i.split("/")[-1]
	f=open(i,'r')
	g=open(outfolder+"/"+name,'w')
	for x in SeqIO.parse(f,'fasta'):
		
		y=x.seq.reverse_complement()
		
		g.write(">"+str(x.description)+"\n"+str(y)+"\n")
		
		
		