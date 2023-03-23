#!/usr/bin/env python3

#theo allnutt 2021
#r3.7 calculates Shannon's information index for sample of reads, only outputs reads over threshold.
#usage
#shannons-filter.py "reads/*" filtered/ 0.8 12 paired 20000000
#filtered/=output folder, 0.8= threshold, 12=threads, paired=paired reads, 20000000 number of reads to sample.
#accepts fasta, fastq and .gz


import sys
import os
import re
import glob
import subprocess as sp
#import multiprocessing
import concurrent.futures
from Bio import SeqIO
import gzip
import math
import collections
from multiprocessing import Manager

digits = re.compile(r'(\d+)')
def tokenize(filename):
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))

def estimate_shannon_entropy(dna_sequence):
	
	seq=dna_sequence.upper()
	if len(seq)-seq.count("N") <=0:
		a=0
		t=0
		c=0
		g=0
	else:
		a=float(seq.count("A")/(len(seq)-seq.count("N")))
		t=float(seq.count("T")/(len(seq)-seq.count("N")))
		c=float(seq.count("C")/(len(seq)-seq.count("N")))
		g=float(seq.count("G")/(len(seq)-seq.count("N")))
	
	if a!=0:
		a1=a * math.log(a,4)
	else: 
		a1=0
	if t!=0:
		t1=t * math.log(t,4)
	else: 
		t1=0
	if c!=0:
		c1=c * math.log(c,4)
	else: 
		c1=0
	if g!=0:
		g1=g * math.log(g,4)
	else: 
		g1=0		
	
	
	entropy_value = -1 * ( a1 + t1 + c1 + g1 )
	
	#print(a,t,c,g, entropy_value)
	
	return entropy_value

def shan(i):
	
	name1=i.split("/")[-1]
	print(name1)
	ext1=name1.split(".")[-1]
	
	if ext1=="gz":
		#print("gz detected")
		f=gzip.open(i,'rt')
		k=name1.split(".")[-2]
		name1=name1[:-3]
	else:
		f=open(i,'r')
		k=ext1
	
	if k[-1]=="a":
		fmt="fasta"
		#print("fasta")
	if k[-1]=="q":
		fmt="fastq"
		#print("fastq")
	c=0
	n=0
	
	outfile=open(outfolder+"/"+name1,'w')
	for x in SeqIO.parse(f,fmt):
		c=c+1
		if n<=sample:
			shannon = estimate_shannon_entropy(str(x.seq))			
			
			if shannon >=shan_limit:
				n=n+1
				SeqIO.write(x,outfile,fmt)
		else:
			break
				
	print(i,c,"reads",n-1,"passed",str(float(n/c*100))[:4],"% passed")
	outfile.close()

def shanpaired(i,j):
	print(i,j)
	
	name1=i.split("/")[-1]
	name2=j.split("/")[-1]
	
	ext1=name1.split(".")[-1]
	
	if ext1=="gz":
		#print("gz detected")
		f1=gzip.open(i,'rt')
		f2=gzip.open(j,'rt')
		k=name1.split(".")[-2]
		name1=name1[:-3]
		name2=name2[:-3]
	else:
		f1=open(i,'r')
		f2=open(j,'r')
		k=ext1
	
	if k[-1]=="a":
		fmt="fasta"
		#print("fasta")
	if k[-1]=="q":
		fmt="fastq"
		#print("fastq")
		
	c=0
	n=0
	
	outfile1=open(outfolder+"/"+name1,'w')
	outfile2=open(outfolder+"/"+name2,'w')
	
	#= SeqIO.to_dict(SeqIO.parse(f1, fmt))
	# = SeqIO.to_dict(SeqIO.parse(f2, fmt))
	
	if fmt=="fastq":
		
		#print(f1,f2)
		while True:
			try:
				if n<=sample:
					a=f1.readline()
					b=f2.readline()
				else:
					break
			except:
				break
			try:
				if a[0]=="@":
					desc1=a
					desc2=b
					seq1=f1.readline().rstrip("\n")
					seq2=f2.readline().rstrip("\n")
					f1.readline()#ignore +
					f2.readline()
					qual1=f1.readline()
					qual2=f2.readline()
					
					c=c+1
					shannon1 = estimate_shannon_entropy(seq1)			
					shannon2 = estimate_shannon_entropy(seq2)	
					#print(seq1,shannon1)
					#print(seq2,shannon2)
					
				
					if shannon1 >=shan_limit and shannon2 >=shan_limit:
						n=n+1
						outfile1.write(desc1+seq1+"\n"+"+"+"\n"+qual1)
						outfile2.write(desc2+seq2+"\n"+"+"+"\n"+qual2)
					#else:
						#print("failed R1",seq1,shannon1)
						#print("failed R2",seq2,shannon2)
						
						
			except:
				break
				
		print(name1,name2,c,"reads",n,"passed",str(float(n/c*100))[:4],"% passed")
		outfile1.close()
		outfile2.close()
	
	
	
folder=sys.argv[1] 
filelist=glob.glob(folder)
filelist.sort(key=tokenize)
print(filelist)
outfolder = sys.argv[2] #outfolder
shan_limit=float(sys.argv[3])
threads=int(sys.argv[4])
ispaired=sys.argv[5]
sample=int(sys.argv[6])

p0=sp.Popen("mkdir -p %s" %outfolder,shell=True).wait()

if __name__ == '__main__':
	
	if ispaired!="paired":
		executor = concurrent.futures.ProcessPoolExecutor(threads)
		futures = [executor.submit(shan, i) for i in filelist]
		concurrent.futures.wait(futures)
					
	else:
		print("paired currently for fastq only! (not interleaved)")
		executor = concurrent.futures.ProcessPoolExecutor(threads)
		futures = [executor.submit(shanpaired, filelist[k],filelist[k+1]) for k in range(0,len(filelist)-1,2)]
		concurrent.futures.wait(futures)
				
	'''	
	for k in range(0,len(filelist)-1,2):
		
		i=filelist[k]
		j=filelist[k+1]
		shanpaired(i,j)
	'''
	
	
	
	#for i in filelist:
		#shan(i)

	#print(data)




		