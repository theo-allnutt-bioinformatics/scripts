#!/usr/bin/env python

#theo allnutt 2019
#gets the lca from a blast fmt 6 output with taxonomy and ranks in last column, from acc2tax.py

#root|cellular organisms|Bacteria|Proteobacteria|Gammaproteobacteria|Enterobacterales|Enterobacteriaceae|Escherichia|Escherichia coli|Escherichia coli O83:H1|Escherichia coli O83:H1 str. NRG 857C	
#no rank|no rank|superkingdom|phylum|class|order|family|genus|species|no rank|no rank
#made in project 075.10

import sys
import os
import re
import glob

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
				  
folder=sys.argv[1] #ublast, acc2tax.py result file
filelist=glob.glob(folder)
filelist.sort(key=tokenize)
print filelist

minpid = int(sys.argv[2]) #int(sys.argv[3]) #minimum %id to accept 

pidr = float(sys.argv[3]) #float(sys.argv[4]) #percent identity radius to accept read hits into LCA algorithm, suggest 3

data={}

for file in filelist:
	print file
	
	f=open(file,'r')
	g=open(file.split(".")[0]+".lca",'w')

	#store each successive lca in data
	
	x=f.readline() #get first line
	
	data["readname"]=x.split("\t")[0].split(" ")[0]
	data["tax"]=x.split("\t")[-1].rstrip("\n").split("|")
	data["toppid"]=float(x.split("\t")[2])
	
	c=0
	t1=1
	while x:
		
		x=f.readline()
		
		if len(x)>1 and x[0]<>"\t":
			
			readname=x.split("\t")[0].split(" ")[0]
			pid=float(x.split("\t")[2])
			tax=x.split("\t")[-1].split("|")
			
		else:
			
			break
		
		if readname==data["readname"] and pid>=minpid and data["toppid"]-pid <=pidr:
			t1=t1+1
			lin1=data["tax"]
			lin2=tax
			
			c=-1
			for j in lin1: #get lca sequencially
				c=c+1
				if c <len(lin2):
					if j<> lin2[c]:
						data["tax"]=lin1[:c]
						break
				else:
					data["tax"]=lin1[:c]
					break
					
		if readname<>data["readname"]: #reached end of read hit list.. therefore data is now lca
			
			g.write("|".join(str(p) for p in data["tax"])+"\t"+str(1)+"\n") #n.b. change 't1' to '1' because t1 was counting reads more than once.
			data["toppid"]=pid
			#assign new read hit
			data["readname"]=x.split("\t")[0].split(" ")[0]
			data["tax"]=x.split("\t")[-1].rstrip("\n").split("|")
			data["toppid"]=float(x.split("\t")[2])
			t1=1
			
			

			
			
			



