#!/usr/bin/env python3

import sys

f = open(sys.argv[1],'r')
g= open(sys.argv[2],'w')

for x in f:

	if x[0]==">":
	
		k=x.split("gene=")[1].split("]")[0]
		g.write(">gene-"+k+"\n")
	else:
		g.write(x)
		