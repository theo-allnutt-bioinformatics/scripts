#!/usr/bin/env python

#written for 082
#use with simabund.py to make the abundance files

import sys
import os
import subprocess
import re
import glob
from random import randrange
import multiprocessing
import concurrent.futures

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
def getreads(abund_file):
	f=open(abund_file,'r')
	
	name1=abund_file.split("/")[-1].split(".")[0]
	
	g=open(outfolder+"/"+name1+".fasta",'w')
	
	for x in f:
	
		seqfile=x.split("\t")[0]
		
		abund=float(x.split("\t")[1].rstrip("\n"))
		
		numreads=abund*totalreads
		
		if numreads<1:
			print seqfile,0,"less than one read, none written"
			break
			
		#get genome(s)
		print "getting reads from", seqfile
		
		try:
		
			h=open(seqfile,'r')
			
		except:
			print "cannot open", seqfile
			break
		
		seq=""
		for i in h:
		
			if i[0]<>">":
			
				seq=seq+i.rstrip("\n")
		#get reads	
		n=0
		
		for j in range(1,int(numreads+1)):
			
			rstart=randrange(0,len(seq)-readlen)
			
			read1 = seq[rstart:rstart+readlen]
			
			#mutate
			g.write(">"+seqfile.split("/")[-1].split(".")[0]+"_"+str(j)+"\n")
			c=-1
			for x in read1:
				c=c+1
				r1=randrange(int(1/mutrate))
				
				if r1==1:
					g.write(bases[randrange(4)])
				else:
					g.write(x)
			g.write("\n")				  

folder=sys.argv[1] 
filelist=glob.glob(folder)
filelist.sort(key=tokenize)

outfolder=sys.argv[2]

readlen=int(sys.argv[3])

totalreads=float(sys.argv[4])

mutrate=float(sys.argv[5])

threads=int(sys.argv[6])

bases=["A","T","C","G","N"]

print filelist


executor = concurrent.futures.ProcessPoolExecutor(threads)
futures = [executor.submit(getreads, abund_file) for abund_file in filelist]
concurrent.futures.wait(futures)



				
			
					
			
			
			
		
		
		
		









