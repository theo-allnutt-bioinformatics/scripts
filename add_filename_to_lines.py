#!/usr/bin/python
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
outfolder=sys.argv[2]

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

t=sys.argv[3]

for i in filelist:

	f=open(i,'r')
	name=i.split("/")[-1]
	g=open(outfolder+"/"+name,'w')
	
	for x in f:
	
		if t=='fasta' and x[0]==">":
		
			g.write(">"+name+x[1:])
		if t=='fasta' and x[0]<>">":	
			g.write(x)
		
			
		if t<>'fasta':
		
			g.write(name+x)