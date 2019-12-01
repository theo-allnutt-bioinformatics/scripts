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

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

outfolder=sys.argv[2]

outsuffix=sys.argv[3]

db=sys.argv[4]
db1=db+".edx"
db2=db+".acx"

pid=sys.argv[5]

threads=sys.argv[6]
print filelist

for i in filelist:
	print i
	
	outputfile=outfolder+"/"+i.split("/")[-1].split(".")[0]+outsuffix+".burst"
	
	p1= sp.Popen("/stornext/HPCScratch/home/allnutt.t/bin/BURST/bin/burst_linux_DB15 -r %s -a %s -q %s -o %s -fr -w -m FORAGE -i %s -t %s -n --skipambig" %(db1,db2,i,outputfile,pid,threads), shell=True).wait() 

