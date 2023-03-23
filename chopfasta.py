#!/usr/bin/env python3
import sys
import os
import re
import glob
from Bio import SeqIO
import subprocess as sp
import concurrent.futures

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  

def chop(i,chopsize,g):


	print(i)
	name1=i.split("/")[-1].split(".")[0]
	h=open(g+"/"+name1+"_chop"+str(chopsize)+".fasta",'w')
	for x in SeqIO.parse(i,'fasta'):
		
		t=0
		
		for c in range(0,len(x.seq),chopsize):
			t=t+1
			id1=x.id+"-chop-"+str(t)
			
			en=c+chopsize
			
			if en > len(x.seq):
				h.write(">"+id1+"\n"+str(x.seq)[c:]+"\n")
				break
				
			else:
				
				h.write(">"+id1+"\n"+str(x.seq)[c:en]+"\n")

			
if __name__ == '__main__':

	folder = sys.argv[1] #working folder

	g=sys.argv[2] #output folder

	chopsize=int(sys.argv[3])
	
	threads=int(sys.argv[4])

	filelist=glob.glob(folder)

	filelist.sort(key=tokenize)

	print(filelist)

	sp.Popen("mkdir -p ./%s" %g,shell=True).wait()	

	executor = concurrent.futures.ProcessPoolExecutor(threads)
	futures = [executor.submit(chop, i,chopsize,g) for i in filelist]
	concurrent.futures.wait(futures)			
			
			
			
			
			
			
			
			
			
			
			
			
			