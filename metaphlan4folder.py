#!/usr/bin/env python3

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

db=sys.argv[4]

threads=sys.argv[5]

type1 = "rel_ab_w_read_stats"

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

p0=subprocess.Popen("mkdir -p %s" %g,shell=True).wait()
p2=subprocess.Popen("module load bowtie2", shell=True).wait()

print(filelist)

for i in filelist:
	print(i)
	name =i.split("/")[-1]
	
	outname=g+"/"+name+".txt"
	
	p1=subprocess.Popen(f"metaphlan {i} -o {outname} --input_type {fmt} --nproc {threads} -t {type1} --tax_lev a --no_map --bt2_ps very-sensitive-local --min_alignment_len 50 --bowtie2db {db} -x mpa_vOct22_CHOCOPhlAnSGB_202212 --tmp_dir ./ --add_viruses --mpa3",shell=True).wait()
	

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			