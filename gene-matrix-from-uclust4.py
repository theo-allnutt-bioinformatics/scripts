#!/usr/bin/python
import os
import re
import glob
import sys
import subprocess
	

#T. Allnutt, CSIRO, 2015
#script to parse the uclust .uc file and make a table of clusters with their %identity
#usage: gene-matrix-from-uclust2.py clusters_sorted.uc pangenome.txt 60 -cds-
#nb '95' is the identiy threshold below which presence of a gene is not scored

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
			  
			  
f = open(sys.argv[1],'r')

g = open(sys.argv[2],'w')

delim = sys.argv[3]

min_samples=int(sys.argv[4])

min_sum=int(sys.argv[5])

data = {}
hitlist=[]
c=1
ct=0
n=0
print "Parsing uc file"
for line in f:
	k = line.split("\t")
	if k[0]<>"C":
		
		hit=k[8].split(delim)[0] #nb the delim separates the cds number from the genome id, so only score the genome id as a hit
		
		
		if hit not in hitlist:
			hitlist.append(hit)
	
	
		if k[0]=="S":
			n=0
			ct=ct+1	
			cds = k[8]
			data[cds]={} #new cluster
			data[cds][hit]=1 #self identity
				
		if k[0]=="H":
			
			n=n+1
				
			if hit not in data[cds].keys():				
					data[cds][hit]=1
					
			else: 
				
				data[cds][hit]=data[cds][hit]+1
		
				
				
print "writing"
hitlist.sort(key=tokenize)		

title="\t"+"\t".join(str(p)for p in hitlist)+"\n"
g.write(title)
output=""
for i in data.keys():
	#sample count
	sample_count=0
	gene_sum=0
	
	
	
	for t in data[i].values():
		if t>0:
			sample_count=sample_count+1
	
	for t in data[i].values():
			gene_sum=gene_sum+t	
		
	
	if gene_sum >= min_sum and sample_count >= min_samples:
		
		c=c+1
		
		g.write(i)
		
		for j in hitlist:
			if j in data[i].keys():
				g.write("\t"+str(data[i][j]))
			else:
				g.write("\t"+"0")
				
		g.write(output+"\n")
		
		

	
		
















	