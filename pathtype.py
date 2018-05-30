#!/usr/bin/python
from __future__ import division
import sys
import re
import glob
import subprocess
from random import randrange
import math
r2=str(randrange(10000))

#Theo Allnutt, 2016
#Find E. coli virulence genes using local version of CGE database (https://cge.cbs.dtu.dk/services/VirulenceFinder/)
#Usage:
#python pathtype.py in/ vir_ecoli 95 80 blastn
#'in' is folder of assemblies in fasta format
#vir_ecoli is a blast db of virulence genes
#95 is min %ID of hit
#80 is min % length of hit

#see vir_matchtype.py in order to attach gene names to db entries before building with makeblastdb

def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token
		for token, match in((fragment, digits.search(fragment))
			for fragment in digits.split(filename)))

#nb the database annotation must be in the sequence id after a " " e.g. >seq1 rage_proteinXF5

folder = sys.argv[1] 

filelist=glob.glob(folder+"/*")
filelist.sort(key=tokenize)
#print filelist
db = sys.argv[2] #ref db to blast against

g= sys.argv[3]

pid =int(sys.argv[4]) #%id threshold
plen=int(sys.argv[5])	#%of subject length threshold

blast_type=sys.argv[6]
# 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'
out = "temp%s.blast" %r2
data={}
names=[]
genes=[]
b=(0,0)
c=0
for f in filelist:
	name=f.split("/")[-1].split(".")[0]
	data[name]={}
	names.append(name)
	loci=[]
	
	print f,blast_type
	if blast_type == "blastp":
		p1= subprocess.Popen("blastp -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -num_threads 24 -evalue 1e-10" %(f,db,out), shell=True).wait()

	if blast_type == "blastn":
		p1= subprocess.Popen("blastn -task blastn -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -num_threads 24 -evalue 1e-10" %(f,db,out), shell=True).wait()
	
	if blast_type == "mega":
		p1= subprocess.Popen("blastn -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -num_threads 24 -evalue 1e-10" %(f,db,out), shell=True).wait()

	
	if blast_type == "blastx":
		p1= subprocess.Popen("blastx -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -num_threads 24 -evalue 1e-10" %(f,db,out), shell=True).wait()
	
		
	result = open(out,'r')
	c=0
	result.seek(0)
	
	new_range=0
	#p1.wait()
	for i in result:	
		k=i.split("\t")
		
		start = int(k[5])
		end=int(k[6])
		if start >end:
			z=end
			end=start
			start=z
		b=(start,end)
		
		
		
		info=k[-1].rstrip("\n")
		gene=k[1]+" "+info#.split("|")[0]
		locus=k[0]
		pchit=float(k[2])
		pclen=float(float(k[3])/float(k[4]))*100
		#print gene, pclen
		
		if locus not in data[name].keys() and pchit>=pid and pclen>= plen:
			loci_ranges=[]
			loci_ranges.append(b)
			loci.append(locus)
			data[name][locus]=[]
			data[name][locus].append(gene)
			data[name][locus].append(pchit)
			data[name][locus].append(pclen)
			data[name][locus].append(start)
			data[name][locus].append(end)
			data[name][locus].append(info)
			genes.append(gene)
			c=0
		if locus in data[name] and pchit>=pid and pclen>= plen:
		#test loci range:
			for t in loci_ranges:
				
				if start>t[1] or end<t[0]:
					new_range=1
				else:
					new_range=0
					break
		if new_range==1:
			loci_ranges.append(b)
			c=c+1
			
			locus=locus+"_"+str(c)
			loci.append(locus)
			data[name][locus]=[]
			data[name][locus].append(gene)
			data[name][locus].append(pchit)
			data[name][locus].append(pclen)
			data[name][locus].append(start)
			data[name][locus].append(end)
			data[name][locus].append(info)
			genes.append(gene)
			new_range=0
		
			

genes=list(set(genes))	
genes.sort(key=tokenize)	

#write detail files
for n in names:
	outfile=open(g+"/"+n+".txt",'w')
	outfile.write("Contig\tGene\t%Identity\t%Length\tStart\tEnd\tProtein\n")
	for i in data[n].keys():
		
		outfile.write("%s\t%s\n" %(i,"\t".join(str(p) for p in data[n][i])))
print genes		


#write summary table
h=open(g+"/"+db.split("/")[-1]+"_"+"summary.txt",'w')
h.write("\t"+"\t".join(str(p) for p in genes)+"\n")
hit=0
for i in names:

	h.write(i)
	
	for j in genes:
		
		for x in data[i].keys():
			
			if data[i][x][0]==j:
				#proportion of matched bases of whole gene
				pchit2=data[i][x][1]/100 * data[i][x][2]/100
				hit=1
				break
			else:
				hit=0
		if hit==0:
			h.write("\t0")
		else:
			h.write("\t"+str(pchit2))
			hit=0
	
	h.write("\n")


p5= subprocess.Popen("rm temp%s.blast" %r2, shell=True).wait() 

		
		