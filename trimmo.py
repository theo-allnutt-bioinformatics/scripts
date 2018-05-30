#!/usr/bin/python

#trimmomatic python wrapper for folders

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

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

threads=sys.argv[2]
adaptors=sys.argv[3]
num=sys.argv[4] #s=single unpaired file, p = paired two files
multi=sys.argv[5]
devnull = open(os.devnull, 'wb')

if num=="s":
	print "Trimmomatic single end mode"
	p0=subprocess.Popen("mkdir -p clip", shell=True).wait
	for i in filelist:
		print i
		name = i.split("/")[-1]
		if multi=="y":
			p1= subprocess.Popen("java -jar ~/bin/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads %s %s clip/%s ILLUMINACLIP:%s:2:30:10 SLIDINGWINDOW:5:25 MINLEN:100" %(threads,i,name,adaptors), shell=True,stderr=devnull)
		if multi=="n":
			p1= subprocess.check_output("java -jar ~/bin/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads %s %s clip/%s ILLUMINACLIP:%s:2:30:10 SLIDINGWINDOW:5:25 MINLEN:100" %(threads,i,name,adaptors), shell=True,stderr=devnull)
		
if num=="p":
	print "Trimmomatic paired end mode"
	p0=subprocess.Popen("mkdir -p clip && mkdir -p unpaired", shell=True).wait
	for i in xrange(0,len(filelist)-1,2):
		print filelist[i],filelist[i+1]
		
		name1 = filelist[i]
		name2 = filelist[i+1]
		outname1 = filelist[i].split("/")[-1]
		outname2 = filelist[i+1].split("/")[-1]
		if multi=="y":
			p1= subprocess.Popen("java -jar ~/bin/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads %s %s %s clip/%s unpaired/%s clip/%s unpaired/%s ILLUMINACLIP:%s:2:30:10 SLIDINGWINDOW:5:25 MINLEN:100" %(threads,name1,name2,outname1,outname1,outname2,outname2,adaptors), shell=True,stderr=devnull)
		if multi=="n":
			p1= subprocess.check_output("java -jar ~/bin/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads %s %s %s clip/%s unpaired/%s clip/%s unpaired/%s ILLUMINACLIP:%s:2:30:10 SLIDINGWINDOW:5:25 MINLEN:100" %(threads,name1,name2,outname1,outname1,outname2,outname2,adaptors), shell=True,stderr=devnull)

print "done"	
		