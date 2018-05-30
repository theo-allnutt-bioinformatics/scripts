#!/home/theoa/qiime-env/env/bin/python

import sys
from fuzzysearch import find_near_matches

ref=open(sys.argv[1],'r')

f = open(sys.argv[2],'r')

g = open(sys.argv[3],'w')

#start=int(sys.argv[4])
#end=int(sys.argv[5])

mm=int(sys.argv[4])

g.write("refseq\ttarget\trank\tmismatches\n")

for x in ref:

	refseq=x.split("\t")[0].rstrip("\n")
	#rank1=x.split("\t")[1].rstrip("\n")
	
	f.seek(0)
	c=0
	for y in f:
		
		c=c+1
		query=y.split("\t")[0].rstrip("\n")#[start:end]
		
		match1=find_near_matches(refseq,query,max_l_dist=mm)

		if match1<>[]:
			
			g.write(refseq+"\t"+query+"\t"+str(c)+"\t"+str(match1[0].dist)+"\n")
			#g.write(refseq+"\t"+rank1+"\t"+query+"\t"+str(c)+"\t"+str(match1[0].dist)+"\n")
			break
		
	if match1==[]:
		
		g.write(refseq+"\tNA\t"+"not found"+"\n")
		#g.write(refseq+"\t"+rank1+"\tNA\t"+"not found"+"\n")			
					
					
					
					
					
					
					
					
					
			
