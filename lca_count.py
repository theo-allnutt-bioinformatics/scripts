#!/usr/bin/env python

import sys
import os
import re
import glob
#made in project 075.10

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#makes an otu table from input species lists

folder = sys.argv[1] #working folder
outfile=sys.argv[2] #output file prefix

#delim=sys.argv[3] #taxonomy output delimiter

fthresh=int(sys.argv[3]) #threshold of number of samples that have each otu
otuthresh=int(sys.argv[4])#total count threshold for each otu

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

print filelist

data={}
allspecies={}
tax_levels=["|superkingdom_","|kingdom_","|phylum_","|order_","|family_","|genus_","|species_"]
filenames=[]

for i in filelist:

	file1 = open(i,'r')
	filename = ".".join(str(p) for p in i.split("/")[-1].split(".")[:-1])
	filenames.append(filename)
	data[filename]={}
	
	#example input format
	#|no rank__root|no rank__cellular organisms|superkingdom__Eukaryota|no rank__Opisthokonta|kingdom__Fungi|subkingdom__Dikarya|phylum__Ascomycota|no rank__saccharomyceta|subphylum__Pezizomycotina|no rank__leotiomyceta|class__Eurotiomycetes|subclass__Eurotiomycetidae|order__Eurotiales|family__Aspergillaceae|genus__Aspergillus|species__Aspergillus flavus|no rank__Aspergillus flavus NRRL3357
	
	for line in file1:
	
		for level in tax_levels:
			if level not in allspecies.keys():
				allspecies[level]=[]
			if level not in data[filename].keys():
				data[filename][level]={}
			if line[0]<>"#":
				fulltax = line.split("\t")[0]
				lowest_tax=fulltax.split("|")[-1]  
				
				levs=[]
				for p in fulltax.split("|"):
					levs.append("|"+p.split("__")[0]+"_")
				
				freq= int(line.split("\t")[-1].rstrip("\n").rstrip("\r"))
			
			
				if level in levs: #lev==level: #n.b. this undercounted higher levels.. 
					
					k1=fulltax.split("|")[:levs.index(level)+1]
					levtax="|".join(str(p) for p in k1)
					
					
					if levtax not in allspecies[level]:
						allspecies[level].append(levtax)
					
					if levtax not in data[filename][level].keys():
						
						data[filename][level][levtax]=freq
						
					else:
						
						data[filename][level][levtax]=data[filename][level][levtax]+freq
			
	file1.close()

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
	lname=level.lstrip("|")
	print level,"###########################################################"
	g2=open(outfile+"_"+lname+".tab",'w')

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
	
	
	
	
	
	
	