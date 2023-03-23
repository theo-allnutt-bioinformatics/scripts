#!/usr/bin/env python3
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
print(filelist)

ref=sys.argv[2]

outfolder=sys.argv[3]

paired=sys.argv[4] 

threads=sys.argv[5]

p0 = subprocess.Popen('mkdir -p %s' %(outfolder), shell=True)
p3 = subprocess.Popen('mkdir -p %s/unmapped' %(outfolder), shell=True)
p3 = subprocess.Popen('mkdir -p %s/mapped' %(outfolder), shell=True)
	

unmappedfolder=outfolder+"/unmapped/"
mappedfolder=outfolder+"/mapped/"

if paired=="unpaired": #unpaired
	for i in filelist:
		
		name=i.split("/")[-1].split(".")[0]
	
		p1= subprocess.Popen("bbmap.sh ref=%s ambig=best nzo=t mappedonly=t outu=%s%s.fasta outm=%s%s.fasta scafstats=%s%s.map in=%s overwrite=t -Xmx64g threads=%s" %(ref,unmappedfolder,name,mappedfolder,name,mappedfolder,name,i,threads), shell=True).wait() #out=mapped/%s.sam && samtools view -bSh1 mapped/%s.sam | samtools sort -m 80G -@ 3 -o mapped/%s_sorted.bam && samtools index mapped/%s_sorted.bam && rm mapped/%s.sam " %(ref,name,name,i,name,name,name,name,name)
		
		#perfectmode=f  
		#maxindel=0 
		#
		
if paired=="paired": #paired two file
	for i in range(0,len(filelist)-1,2):

		name1 = filelist[i].split("/")[-1]
		name2 = filelist[i+1].split("/")[-1]
	
		
		print(filelist[i],filelist[i+1])
		

		p1= subprocess.Popen("bbmap.sh ref=%s ambig=best nzo=t mappedonly=t scafstats=%s%s.map in1=%s in2=%s outm1=%s%s outm2=%s%s outu1=%s%s outu2=%s%s -Xmx64g overwrite=t threads=%s" %(ref,mappedfolder,name1,filelist[i],filelist[i+1],mappedfolder,name1,mappedfolder,name2,unmappedfolder,name1,unmappedfolder,name2,threads), shell=True).wait() 


		#perfectmode=f  
		#maxindel=0 
		#

if paired=="pairedint": #paired interleaved
	for i in filelist:
		
		name=i.split("/")[-1].split(".")[0]
	
		p1= subprocess.Popen("bbmap.sh ref=%s ambig=all nzo=t mappedonly=t outu=%s%s.fasta outm=%s%s.fasta scafstats=%s%s.map in=%s out=%s/%s interleaved=true overwrite=t threads=%s" %(ref,unmappedfolder,name,mappedfolder,name,mappedfolder,name,i,outfolder,name+".sam",threads), shell=True).wait()
		
		#perfectmode=f  
		#
		#