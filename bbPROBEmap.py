#!/usr/bin/python
import sys
from Bio import SeqIO
import subprocess


#Theo Allnutt, 2017
#bbmaps pcr primers in pairs to find location(s) and orientation

probes = sys.argv[1]
ref = sys.argv[2]
sam=sys.argv[4]
g=open(sys.argv[3],'w') # hits output
id = sys.argv[5]
m=sys.argv[6]

if m=="u":
	p1=subprocess.Popen("bbmap.sh in=%s ref=%s out=%s ordered=t overwrite=t ambiguous=best minid=%s" %(probes,ref,sam,id),shell=True).wait()
else:
	p1=subprocess.Popen("bbmap.sh in=%s ref=%s out=%s ordered=t overwrite=t ambiguous=best minid=%s mappedonly=t" %(probes,ref,sam,id),shell=True).wait()
		
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
		s=int(k[1])
		if s==16:
			orient="-"
		if s==0:
			orient="+"
		if s==4:
			orient="unmapped"
		
		
		if read not in data.keys():
			data[read]=[]
			data[read].extend([scaf,locus,orient])
			
g.write("assay\thit\tlocus\torientation\n")

for i in reads:	
	g.write(i+"\t"+"\t".join(str(x) for x in data[i])+"\n")
	
			
			
			
			
		
		