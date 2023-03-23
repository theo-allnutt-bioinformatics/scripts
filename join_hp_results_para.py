#!/usr/bin/env python3
import sys
import re
import glob
import subprocess as sp
import os
import concurrent.futures

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

#geneName.paralogs.fasta

def join_paralogs(i):
	

	files1=os.listdir(resdir+i+"/paralogs_all/")
	
	print(i)
	for j in files1:
		j1=j.replace("_paralogs_all",".paralogs")
		#print("Joining %s/paralogs_all/" %i,j)
		p2=sp.Popen("cat %s/%s/paralogs_all/%s >> %s/all_paralogs_joined/%s" %(resdir,i,j,resdir,j1),shell=True).wait()
		
	files2=os.listdir(resdir+i+"/paralogs_no_chimeras/")
	
	for j in files2:
		j1=j.replace("_paralogs_all",".paralogs")
		#print("Joining %s/paralogs_no_chimeras/" %i,j)
		p3=sp.Popen("cat %s/%s/paralogs_no_chimeras/%s >> %s/paralogs_no_chimeras_joined/%s" %(resdir,i,j,resdir,j1),shell=True).wait()
	
	
	#head -2 results/EG98/EG98_stats.tsv |tail -1 
	print("Joining stats",i)
	p4=sp.Popen("head -2 %s/%s/%s_stats.tsv |tail -1 >> %s/stats_joined.txt" %(resdir,i,i,resdir),shell=True).wait
	
def get_lengths():
	
	for i in dirs:
	
		g2=open(resdir+"/"+i+"/"+i+"_lengths.tsv",'r')
		#each file genes are in different order
		
		#genes
		genes=[]
		
		k=g2.readline().rstrip("\n").split("\t")[1:]
		
		for x in k:
		
			genes.append(x)
		
			if x not in allgenes:
				allgenes.append(x)
				
		#means only for first file, should all be the same
		if len(lens.keys())<2:
			
			k=g2.readline().rstrip("\n").split("\t")[1:]
			c=-1
			for x in k:
				if x not in means.keys():
					c=c+1
					means[genes[c]]=x
					
		else:
			g2.readline() #skip means other than first file
				
		#lengths
		lens[i]={}
		k=g2.readline().rstrip("\n").split("\t")[1:]
		c=-1
		if i not in species:
			species.append(i)
			
		for x in k:
			c=c+1
			lens[i][genes[c]]=x
				
		g2.close()
		
		
	#return genes,lens


################global

resdir=sys.argv[1]
threads=int(sys.argv[2])
dirs=next(os.walk(resdir))[1]

if "paralogs_no_chimeras_joined" in dirs:
	dirs.remove("paralogs_no_chimeras_joined")
if "all_paralogs_joined" in dirs:
	dirs.remove("all_paralogs_joined")

print("N.B. deleting any existing directories of joined files")

p0=sp.Popen("rm -rf %s/all_paralogs_joined/" %resdir,shell=True).wait()
p1=sp.Popen("rm -rf %s/paralogs_no_chimeras_joined/" %resdir,shell=True).wait()

p0=sp.Popen("mkdir -p %s/all_paralogs_joined/" %resdir,shell=True).wait()
p1=sp.Popen("mkdir -p %s/paralogs_no_chimeras_joined/" %resdir,shell=True).wait()

g1=open(resdir+"/stats_joined.txt",'w')
g1.write("Name\tNumReads\tReadsMapped\tPctOnTarget\tGenesMapped\tGenesWithContigs\tGenesWithSeqs\tGenesAt25pct\tGenesAt50pct\tGenesAt75pct\tGenesAt150pct\tParalogWarningsLong\tParalogWarningsDepth\tGenesWithoutStitchedContigs\tGenesWithStitchedContigs\tGenesWithStitchedContigsSkipped\tGenesWithChimeraWarning\n")
g1.close()

lens={}
species=[]
genes=[]
means={}
allgenes=[]

if __name__ == '__main__':
	
	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(join_paralogs,i) for i in dirs]
	concurrent.futures.wait(futures1)
	
	#get lengths
	print("Getting lengths")
	get_lengths()
	
	
	#print(genes)
	#print(lens)
	
	allgenes.sort(key=tokenize)

	g3=open(resdir+"/"+"all_lengths.txt",'w')

	g3.write("Species\t"+"\t".join(str(p) for p in allgenes)+"\n")

	g3.write("MeanLength\t")
	#print(lens)
	#print('genes',genes)
	for x in allgenes:
		g3.write(means[x]+"\t")
	g3.write("\n")

	species.sort(key=tokenize)

	for x in species:
		g3.write(x)
		for y in allgenes:
		
			if y in lens[x].keys():
				g3.write("\t"+lens[x][y])
				
			else:
				g3.write("\t0")
			
		g3.write("\n")
		
	g3.close()

	print("Done")