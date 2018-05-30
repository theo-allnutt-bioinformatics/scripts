#!/usr/bin/python
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

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

print filelist

for i in filelist:
	print i
	name =i.split("/")[-1]
	
	outname=g+"/"+name+".txt"
	
	p1=subprocess.Popen("metaphlan2.py %s -o %s --input_type %s --nproc 32 -t rel_ab_w_read_stats --tax_lev a --no_map --bt2_ps very-sensitive-local --min_alignment_len  50" %(i,outname,fmt),shell=True).wait()
	

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			