#!/usr/bin/env python
import sys
import re
import glob
import subprocess
import os

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


folder = sys.argv[1] 
folder = os.path.expanduser(folder)

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
for i in filelist:
	print i;
	
outfolder=sys.argv[2]

subprocess.Popen("mkdir -p %s" %outfolder,shell=True).wait()
subprocess.Popen("module load kraken2",shell=True).wait()

outsuffix=sys.argv[3]

conf= sys.argv[4]

threads=sys.argv[5]

db= sys.argv[6]

for i in filelist:
	print 'Processing:',i
	rootname=i.split("/")[-1].split(".")[0]
	outname=outfolder+"/"+rootname+outsuffix
	outnohits=outfolder+"/"+rootname+outsuffix
	
	subprocess.Popen("/stornext/System/data/apps/kraken2/kraken2-2.0.7-beta/bin/kraken2 --db %s %s --threads %s --classified-out %s_hits.fa --confidence %s --report %s.report --use-mpa-style --use-names -output %s.out --unclassified-out %s.nohit.fasta" %(db,i,threads,outname,conf,outname,outname,outnohits),shell=True).wait()





