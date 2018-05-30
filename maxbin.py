#!/usr/bin/python
import sys
import re
import glob
import subprocess


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))



folder = sys.argv[1] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

readsfolder=sys.argv[2]
reads=glob.glob(readsfolder)

reads.sort(key=tokenize)
print reads


size=sys.argv[3]

p3 = subprocess.Popen('mkdir -p ./maxbin', shell=True)

c=-1

for i in filelist:
	c=c+1
	name=i.split("/")[-1].split(".")[0]
	
	readfile=reads[c]
	print 'binning', i, 'using read file', readfile
	
	p1= subprocess.Popen("run_MaxBin.pl -thread 8 -contig %s -out maxbin/%s -reads %s -min_contig_length %s" %(i,name+".txt",readfile,size), shell=True).wait()
	
	
	
	
	
	
	
	