#!/usr/bin/python
import sys
from Bio import SeqIO
import subprocess


#Theo Allnutt, 2017
#bbmaps pcr primers in pairs to find location(s) and orientation

primers = sys.argv[1]
ref = sys.argv[2]
g=open(sys.argv[3],'w') # hits output
sam=sys.argv[4]
maxlen = sys.argv[5]

id = sys.argv[6]

p1=subprocess.Popen("bbmap.sh in=%s ref=%s out=%s ordered=t overwrite=t interleaved=t ambiguous=all pairedonly=t pairlen=%s minid=%s" %(primers,ref,sam,maxlen,id),shell=True).wait()
	
h=open(sam,'r')

data={}
reads=[]
for i in h:
	if i[0]<>"@":
		k=i.rstrip("\n").split("\t")
		read=k[0]
		if read not in reads:
			reads.append(read)
		scaf=k[2]
		locus=k[3]
		s=int(k[8])
		if s<0:
			orient="-"
		else:
			orient="+"
		size=str(abs(s))
		
		if read not in data.keys():
			data[read]=[]
			data[read].extend([scaf,locus,size,orient])
			
g.write("assay\thit\tlocus\tsize\torientation\n")

for i in reads:	
	g.write(i+"\t"+"\t".join(str(x) for x in data[i])+"\n")
	
			
			
			
			
		
		