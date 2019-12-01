#!/usr/bin/env python

import sys
import re
import glob

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


folder = sys.argv[1] 
#folder = os.path.expanduser(folder)

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
outfolder=sys.argv[2]

for i in filelist:
	name1=i.split("/")[-1]
	f =open(i,'r')
	g=open(outfolder+"/"+name1,'w')
	t=0
	for x in f:
		t=t+1
		k=x.split("\t")
		names=k[0].split(" ")
		abund=k[-1]
		
		if len(names)>1:
			outname=names[0]+" "+names[1]
		
		else:
			outname=names[0]
			
		g.write(outname+"\t"+abund)
		

