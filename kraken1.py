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
subprocess.Popen("module load kraken/1.1",shell=True).wait()

threads=sys.argv[3]

db= sys.argv[4]

for i in filelist:
	print 'Processing:',i
	rootname=i.split("/")[-1].split("_")[0]
	outname=outfolder+"/"+rootname
	
	subprocess.Popen("kraken --db %s %s --threads %s --classified-out %s_hits.fa --unclassified-out %s_nohits.fa --output %s.out --only-classified-output" %(db,i,threads,outname,outname,outname),shell=True).wait()

	subprocess.Popen("kraken-translate --db %s %s.out --mpa-format > %s.report" %(db,outname,outname),shell=True).wait()





