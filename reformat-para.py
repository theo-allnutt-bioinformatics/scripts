#!/usr/bin/env python3
import sys
import re
import glob
import subprocess as sp
import multiprocessing
import concurrent.futures


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))




def reformat(i,j):

	outfile = outfolder+"/"+i.split("/")[-1].split(".")[0]+"."+fmt #name cannot have '.' before ext
	print(outfile)
	p1=sp.Popen("reformat.sh in1=%s in2=%s out=%s ow=t samplereadstarget=%s fastawrap=1000000" %(i,j,outfile,samples),shell=True).wait()
	
def reformat_single(i):

	outfile = outfolder+"/"+i.split("/")[-1].split(".")[0]+"."+fmt #name cannot have '.' before ext
	print(outfile)
	p1=sp.Popen("reformat.sh in=%s out=%s ow=t samplereadstarget=%s fastawrap=1000000" %(i,outfile,samples),shell=True).wait()

folder = sys.argv[1] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print(filelist)

outfolder=sys.argv[2]

fmt=sys.argv[3]

samples=sys.argv[4]

threads=int(sys.argv[5])	

paired=sys.argv[6]

if paired=="paired":
	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(reformat, filelist[i],filelist[i+1]) for i in range(0,len(filelist)-1,2)]
	concurrent.futures.wait(futures1)

else:
	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(reformat_single, i) for i in filelist]
	concurrent.futures.wait(futures1)	
	
	#for i in filelist:
	
		#reformat_single(i)

	