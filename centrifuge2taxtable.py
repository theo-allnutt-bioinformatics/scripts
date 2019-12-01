#!/usr/bin/env python

import sys
import os
import re
import glob
import subprocess


#Theo Allnutt Bioinformatics, 2019
#Requires tax_trace.pl in path: https://github.com/maxnest/SPbU_work or edit line 100 for location
#also requires ncbi taxonomy files names.dmp and nodes.dmp, available from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
#Usage: centrifuge2taxtable.py "report/*.txt" cent.tab unique species 1 100
#arguments = report folder; output file; level: species, genus etc.; 1 = minimum number of samples with a taxon; 100 = minimum total count of a taxon

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#makes a taxonomy table from folder of centrifuge reports for different levels:


folder = sys.argv[1] #working folder
outfile=sys.argv[2]#output file 
readtype=sys.argv[3] #count type, all or unique
taxtype=sys.argv[4] #species / genus etc.
otuthresh=int(sys.argv[5]) #minimum number of samples with a taxon
countthresh=int(sys.argv[6]) #minimum total count of a taxon

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

print filelist

if readtype=="all":
	d=4
else:
	d=5

data={}
taxa=[]
samples=[]

for i in filelist:
	print i
	f=open(i,'r')
	filename= i.split("/")[-1]
	samplename=filename.split(".")[0]
	samples.append(samplename)
	
	f.readline()
	
	for x in f:
		k=x.split("\t")
		taxid=k[0]+"\t"+k[1]
		count=int(k[d])
		if k[2]=="leaf" or k[2]=="subspecies":
			k[2]=="species"
		
		if k[2]==taxtype:
			
			if taxid not in data.keys():
				if taxid not in taxa:
					taxa.append(taxid)
				data[taxid]={}
				data[taxid][samplename]=count
				
			else:
				data[taxid][samplename]=count
				
#write data	

#g.write("name\ttaxid\t"+"\t".join(str(p) for p in samples)+"\n")

g=open('temp.tab','w') 
n=0
for x in taxa:
	
	otus=len(data[x])
	t=0
	for j in samples:
		if j in data[x].keys():
			t=t+data[x][j]
	totalcount=t
	
	if otus>=otuthresh and totalcount>=countthresh:
		n=n+1
		g.write(x)
		for j in samples:
			if j in data[x].keys():
				g.write("\t"+str(data[x][j]))
			else:
				g.write("\t0")
		g.write("\n")
g.close()
#add full taxonomy
print "adding taxonomy"

p0=subprocess.Popen("cut -f1-2 temp.tab  > tax.in" ,shell=True).wait()


p1=subprocess.Popen("perl /stornext/HPCScratch/home/allnutt.t/scripts/tax_trace.pl /stornext/HPCScratch/home/allnutt.t/db/ncbi_taxonomy/nodes.dmp /stornext/HPCScratch/home/allnutt.t/db/ncbi_taxonomy/names.dmp tax.in tax.out",shell=True).wait()

p3=subprocess.Popen("cut -f1 tax.out | paste temp.tab - > %s " %(outfile),shell=True).wait()
p4=subprocess.Popen("sed -i '1iname\ttaxid\t%s\n' %s" %("\t".join(str(p) for p in samples),outfile),shell=True).wait()
p5=subprocess.Popen("sed -i 's/root|cellular organisms|//g' %s" %outfile,shell=True).wait()
p7=subprocess.Popen("sed -i 's/root|//g' %s" %outfile,shell=True).wait()

p6=subprocess.Popen("rm tax.in tax.out temp.tab",shell=True).wait()

print "Total taxa =", str(len(taxa)), "Filtered taxa =", str(n)
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	