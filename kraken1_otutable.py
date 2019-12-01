#!/usr/bin/env python

import sys
import os
import re
import glob
#written for 75.9 convert kraken reports to otu tables for each taxonmic level

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#makes an otu table from input species lists

folder = sys.argv[1] #working folder
outfile=sys.argv[2] #output file prefix

delim="|" #taxonomy output delimiter

fthresh=int(sys.argv[3]) #threshold of number of samples that have each otu
otuthresh=int(sys.argv[4])#total count threshold for each otu

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

'''
if sys.argv[6] == 'count':
	dtype=-1
else:
	dtype=1
'''

print filelist

data={}
allspecies={}
tax_levels=["d","k","p","c","o","f","g","s","t"]
filenames=[]

for i in filelist:

	file1 = open(i,'r')
	filename = ".".join(str(p) for p in i.split("/")[-1].split(".")[:-1])
	filenames.append(filename)
	data[filename]={}
	
	#A00326:16:HJW33DMXX:2:1104:7030:1736	d__Eukaryota|k__Viridiplantae|p__Streptophyta|o__Asterales|f__Asteraceae|g__Hinterhubera|s__Hinterhubera_ericoides
	
	for line in file1:
	
		for level in tax_levels:
			if level not in allspecies.keys():
				allspecies[level]=[]
			if level not in data[filename].keys():
				data[filename][level]={}
				
			
			sp1 = line.split("\t")[1].rstrip("\n")
			sp=sp1.split(delim)[-1]
			
			lev = sp.split("__")[0]
			
			#freq= float(line.split("\t")[dtype].rstrip("\n").rstrip("\r")) kaken1 does not report counts
			#if dtype==-1:
			#	freq=int(freq)
			
			#if sp1=="unclassified":
			#	if sp1 not in allspecies[level]:
			#		allspecies[level].append(sp1)
				
			#	if sp1 not in data[filename][level]:
					
			#		data[filename][level][sp1]=""
					
			#	data[filename][level][sp1]=freq	
			
			if lev==level:
			
				if sp1 not in allspecies[level]:
					allspecies[level].append(sp1)
				
				if sp1 not in data[filename][level]:
					
					data[filename][level][sp1]=0
					
				data[filename][level][sp1]=data[filename][level][sp1]+1
		
	file1.close()

print data

filenames.sort(key=tokenize)

for v in allspecies.keys():	
	allspecies[v].sort()
#print allspecies

#remove if below threshold
allspecies2={}

for level in tax_levels:
	allspecies2[level]=[]
	for i in allspecies[level]:
		c=0
		otutotal=0
		for j in filenames:
			
			if i in data[j][level].keys():
					c=c+1
					otutotal=otutotal+data[j][level][i]
				
		if c >= fthresh and otutotal>=otuthresh:
			allspecies2[level].append(i)
			
		
g=open(outfile+"_all_"+".tab",'w')

		
for level in tax_levels:
	print level,"###########################################################"
	g2=open(outfile+"_"+level+".tab",'w')

	g.write(level+"\t\t"+"\t".join(str(x) for x in filenames)+"\n")
	g2.write("#OTU_ID"+"\t"+"\t".join(str(x) for x in filenames)+"\n")
	
	for i in allspecies2[level]:
		print (i.split("__")[-1])
		#g.write(i+"\t")  #change to write the whole taxonomy
		g.write(i+"\t"+i.split("__")[-1])
		#g2.write(i) #change to write the whole taxonomy
		g2.write(i.split("__")[-1])
		
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
	
	
	
	
	
	
	