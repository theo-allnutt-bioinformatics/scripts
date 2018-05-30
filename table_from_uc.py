#!/usr/bin/python
import os
import re
import glob
import sys
	

#T. Allnutt, 2017
#script to parse the usearch .uc file and make a table of clusters 
#usage: table_from_uc.py clusters_sorted.uc output.tab . 1 10
#input must be sorted by: sort -nk2 clusters.uc > clusters_sorted.uc
#. = sample name / read number delimiter
#1 = min number of samples in cluster to be retained in table
#100 = min sum of cluster members to be retained in table
#THIS VERSION TAKES 'size=' IN DEFLINES INTO ACCOUNT AS USED IN USEARCH

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
	if k[0]<>"S":
		
		hit=k[8].split(";")[0].split(delim)[0] 
		
		if hit not in hitlist:
			hitlist.append(hit)
		
	
		if k[0]=="C":
			n=0
			ct=ct+1	
			cds = k[8].split(";")[0]
			data[cds]={} #new cluster
			
			if "size=" in k[8]:
				size = int(k[8].split("size=")[1].rstrip(";"))
	
				data[cds][hit]=size #self identity
			else:
				data[cds][hit]=1
				
		if k[0]=="H":
			
			n=n+1
				
			if hit not in data[cds].keys():
				if "size=" in k[8]:
					size = int(k[8].split("size=")[1].rstrip(";"))
				
					data[cds][hit]=size
				else:
					data[cds][hit]=1
					
			else: 
				if "size=" in k[8]:
					size = int(k[8].split("size=")[1].rstrip(";"))
					data[cds][hit]=data[cds][hit]+size
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
		
		

	
		
















	