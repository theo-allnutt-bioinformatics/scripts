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
				
f= open(sys.argv[1],'r')
h= open(sys.argv[2],'r')
g= open(sys.argv[3],'w')


loci=[]
sam={}

for i in f:
	k=i.split("\t")
	loci.append(k[0].rstrip("\n"))
	
loci.sort(key=tokenize)
	
for i in h:

	k=i.split("\t")
	
	mir = k[0]
	loc = k[2]
	
	if loc not in sam.keys():
	
		sam[loc]=[]
		sam[loc].append(mir)
	else:
		sam[loc].append(mir)
n=0	
v=0
for i in loci:

	if i in sam.keys():
		n=n+1
		g.write(i+"\t"+(":".join(str(p) for p in sam[i])+"\n"))
	else:
		v=v+1
		g.write(i+"\tnot found\n")
	
print 'mirs found=', n, 'not found=', v
	
	
	
	
	
	
	
	