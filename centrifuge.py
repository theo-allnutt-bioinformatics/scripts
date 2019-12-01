#!/usr/bin/env python

import sys
import re
import glob
import subprocess as sp
import os


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


folder = sys.argv[1] 
#folder = os.path.expanduser(folder)

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

outfolder=sys.argv[2]

outsuffix=sys.argv[3]

db=sys.argv[4]

threads=sys.argv[5]

stype=sys.argv[6] #f for fasta q for fastq.. unaligned saved reads are fastq
print filelist

for i in filelist:
	print i
	
	outputfile=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".cent"
	reportfile=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".report"
	outnomatch=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".nohit.fasta"
	
	p1= sp.Popen("/stornext/HPCScratch/home/allnutt.t/bin/centrifuge/centrifuge -x %s -U %s -S %s --report-file %s --un %s --min-hitlen 50 -k 1 -p %s -%s --verbose" %(db,i,outputfile,reportfile,outnomatch,threads,stype), shell=True).wait() 

