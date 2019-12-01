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

maxhits=sys.argv[5]

pid=sys.argv[6]

threads=sys.argv[7]
print filelist

for i in filelist:
	print i
	
	outputfile=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".ublast"
	outnomatch=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".nohit.fasta"
	
	p1= sp.Popen("/stornext/HPCScratch/home/allnutt.t/bin/usearch10 -ublast %s -db %s -strand both -maxhits %s -userout %s -userfields query+target+id+ql+qlo+qhi+tl+tlo+thi+alnlen+evalue+bits -id %s -notmatched %s -threads %s -termidd 0.1 -accel 0.1 -evalue 1e-9" %(i,db,maxhits,outputfile,pid,outnomatch,threads), shell=True).wait() 

