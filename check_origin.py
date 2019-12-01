#!/usr/bin/env python

import sys
import re
import glob
import subprocess as sp


#082.3 check origin of abund entry: virus, bact, euk.

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

chklist=open(sys.argv[2],'r')

outfolder=sys.argv[3]

chk=[]
for i in chklist:
	chk.append(i.rstrip("\n"))

for i in filelist:

	f=open(i,'r')
	name1=i.split("/")[-1]
	g=open(outfolder+"/"+name1,'w')
	
	for j in f:
		print j
		k=j.split("\t")[0].split("_")[0]+"_"+j.split("\t")[0].split("_")[1]
		
		if k in chk:
		
			g.write(j)












