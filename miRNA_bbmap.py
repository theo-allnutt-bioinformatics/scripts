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

ref=sys.argv[2]

outfolder=sys.argv[3]

bam=sys.argv[4] #bam file y/n

p3 = subprocess.Popen('mkdir -p %s' %(outfolder), shell=True)
p3 = subprocess.Popen('mkdir -p %s/unmapped' %(outfolder), shell=True)
p3 = subprocess.Popen('mkdir -p %s/mapped' %(outfolder), shell=True)
	

for i in filelist:

	print i
	
	name = i.split("/")[-1].split(".")[0]
	
	if bam=="y":
	
		p1= subprocess.Popen("bbmap.sh ref=%s ambig=all vslow perfectmode maxsites=10000 nzo=t mappedonly=t outu=%s/unmapped/%s.unmapped.fasta scafstats=%s/mapped/%s.map in=%s out=%s/mapped/%s.sam noheader=t " %(ref,outfolder,name,outfolder,name,i,outfolder,name), shell=True).wait() #&& samtools view -bSh1 %s/mapped/%s.sam | samtools sort -m 80G -@ 3 -o %s/mapped/%s_sorted.bam && samtools index %s/mapped/%s_sorted.bam && rm %s/mapped/%s.sam
	
	else:
		p1= subprocess.Popen("bbmap.sh ref=%s ambig=all vslow perfectmode maxsites=10000 nzo=t mappedonly=t outu=%s/unmapped/%s.unmapped.fasta scafstats=%s/mapped/%s.map in=%s" %(ref,outfolder,name,outfolder,name,i), shell=True).wait()
	
	

