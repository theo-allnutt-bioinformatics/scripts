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

num=sys.argv[4] #1=single unpaired file, 2 = paired two files

prefix=sys.argv[5]

id=sys.argv[6]

disk=sys.argv[7]

p3 = subprocess.Popen('mkdir -p %s/%s_unmapped' %(outfolder,prefix), shell=True)
p3 = subprocess.Popen('mkdir -p %s/%s_mapped' %(outfolder,prefix), shell=True)
	

unmappedfolder=outfolder+"/"+prefix+"_unmapped/"
mappedfolder=outfolder+"/"+prefix+"_mapped/"

if num=="1":
	for i in filelist:
		
		name=i.split("/")[-1].split(".")[0]
	
		p1= subprocess.Popen("bbmap.sh maxindel=0 minid=%s ref=%s ambig=best nodisk=%s nzo=t fast=t  mappedonly=t outu=%s%s.unmapped.fasta outm=%s%s.mapped.fasta scafstats=%s%s.map in=%s interleaved=true" %(id,ref,disk,unmappedfolder,name,mappedfolder,name,mappedfolder,name,i), shell=True).wait() #out=mapped/%s.sam && samtools view -bSh1 mapped/%s.sam | samtools sort -m 80G -@ 3 -o mapped/%s_sorted.bam && samtools index mapped/%s_sorted.bam && rm mapped/%s.sam " %(ref,name,name,i,name,name,name,name,name)
		
	
if num=="2":
	for i in xrange(0,len(filelist)-1,2):

		name1 = filelist[i].split("/")[-1].split(".")[0].split("R1")[0]
		name2 = filelist[i+1].split("/")[-1].split(".")[0]
	
		
		print filelist[i],filelist[i+1]
		

		p1= subprocess.Popen("bbmap.sh ref=%s ambig=all nzo=t k=15 fast=t mappedonly=t scafstats=%s%s.map in1=%s in2=%s outu=%s%s.unmapped.fastq" %(ref,mappedfolder,name1,filelist[i],filelist[i+1],unmappedfolder,name1), shell=True).wait() 

if num=="3":
	for i in filelist:
		
		name=i.split("/")[-1].split(".")[0]
	
		p1= subprocess.Popen("bbmap.sh ref=%s ambig=all nodisk=%s nzo=t k=15 fast=t  mappedonly=t outu=%s%s.unmapped.fasta outm=%s%s.mapped.fasta scafstats=%s%s.map in=%s interleaved=false" %(ref,disk,unmappedfolder,name,mappedfolder,name,mappedfolder,name,i), shell=True).wait() #out=mapped/%s.sam && samtools view -bSh1 mapped/%s.sam | samtools sort -m 80G -@ 3 -o mapped/%s_sorted.bam && samtools index mapped/%s_sorted.bam && rm mapped/%s.sam " %(ref,name,name,i,name,name,name,name,name)		
		
		