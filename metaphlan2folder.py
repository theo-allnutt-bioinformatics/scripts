#!/usr/bin/env python
import sys
import os
import re
import glob
import subprocess

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
folder = sys.argv[1] #working folder

g=sys.argv[2] #output folder

fmt=sys.argv[3]

extras=sys.argv[4]

threads=sys.argv[5]

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

p0=subprocess.Popen("mkdir -p %s" %g,shell=True).wait()
p2=subprocess.Popen("module load bowtie2", shell=True).wait()

print filelist

for i in filelist:
	print i
	name =i.split("/")[-1]
	
	outname=g+"/"+name+".txt"
	
	p1=subprocess.Popen("metaphlan2.py %s -o %s --input_type %s --nproc %s -t rel_ab --tax_lev a --no_map --bt2_ps very-sensitive-local --min_alignment_len 50 %s" %(i,outname,fmt,threads,extras),shell=True).wait()
	

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			