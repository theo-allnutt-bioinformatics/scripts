#!/usr/bin/python

import sys
import os
import re
import glob
#written for 060, outputs all taxon levels, use "-t rel_ab_w_read_stats" in metaphlan2.py

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#makes an otu table from insput species lists

folder = sys.argv[1] #working folder
outfile=sys.argv[2] #output file prefix

delim=sys.argv[3] #taxonomy output delimiter

fthresh=int(sys.argv[4]) #otu removal threshold

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

if sys.argv[5] == 'count':
	dtype=-1
else:
	dtype=1

print filelist

data={}
allspecies={}
tax_levels=["p","c","o","f","g","s"]
filenames=[]

for i in filelist:

	file1 = open(i,'r')
	filename = ".".join(str(p) for p in i.split("/")[-1].split(".")[:-1])
	filenames.append(filename)
	data[filename]={}
	
	for line in file1:
		for level in tax_levels:
			if level not in allspecies.keys():
				allspecies[level]=[]
			if level not in data[filename].keys():
				data[filename][level]={}
			if line[0]<>"#":
				sp1 = line.split("\t")[0]
				sp=sp1.split(delim)[-1]
				
				lev = sp.split("__")[0]
				
				freq= float(line.split("\t")[dtype].rstrip("\n").rstrip("\r"))
				if dtype==-1:
					freq=int(freq)
				if sp1=="unclassified":
					if sp1 not in allspecies[level]:
						allspecies[level].append(sp1)
					
					if sp1 not in data[filename][level]:
						
						data[filename][level][sp1]=""
						
					data[filename][level][sp1]=freq	
				
				if lev==level:
				
					if sp1 not in allspecies[level]:
						allspecies[level].append(sp1)
					
					if sp1 not in data[filename][level]:
						
						data[filename][level][sp1]=""
						
					data[filename][level][sp1]=freq
			
	file1.close()

filenames.sort(key=tokenize)

for v in allspecies.keys():	
	allspecies[v].sort()
print allspecies

#remove if below threshold
allspecies2={}
for level in tax_levels:
	allspecies2[level]=[]
	for i in allspecies[level]:
		c=0
		for j in filenames:
			
			if i in data[j][level].keys():
					c=c+1
				
		if c >= fthresh:
			allspecies2[level].append(i)
			
		
g=open(outfile+"_all_"+".tab",'a')

		
for level in tax_levels:

	g2=open(outfile+"_"+level+".tab",'w')

	g.write(level+"\t\t"+"\t".join(str(x) for x in filenames)+"\n")
	g2.write("#OTU_ID"+"\t"+"\t".join(str(x) for x in filenames)+"\n")
	
	for i in allspecies2[level]:
	
		g.write(i+"\t")
		g.write(i.split("__")[-1])
		g2.write(i)
		#g2.write(i.split("__")[-1])
		
		for j in filenames:
		
			if i in data[j][level].keys():
				g.write("\t"+str(data[j][level][i]))
				g2.write("\t"+str(data[j][level][i]))
			else:
				g.write("\t"+"0")
				g2.write("\t"+"0")
			
		g.write("\n")
		g2.write("\n")
	g.write("\n")
	g2.write("\n")
	
	
	
	
	
	
	