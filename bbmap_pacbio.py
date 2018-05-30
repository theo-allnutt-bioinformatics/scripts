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

#mapPacBio.sh

folder = sys.argv[1] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

ref=sys.argv[2]

outfolder=sys.argv[3]

#num=sys.argv[4] #1=single unpaired file or paired if interleaved, 2 = paired two files

prefix=sys.argv[4]


p3 = subprocess.Popen('mkdir -p %s/%s_unmapped' %(outfolder,prefix), shell=True)
p3 = subprocess.Popen('mkdir -p %s/%s_mapped' %(outfolder,prefix), shell=True)
	

unmappedfolder=outfolder+"/"+prefix+"_unmapped/"
mappedfolder=outfolder+"/"+prefix+"_mapped/"

for i in filelist:
		
	name=i.split("/")[-1].split(".")[0]
	
	p1= subprocess.Popen("mapPacBio.sh ref=%s ambig=all nodisk=t nzo=t mappedonly=t outu=%s%s.unmapped.fasta  outm=%s%s.mapped.fasta scafstats=%s%s.map in=%s fastareadlen=6000 " %(ref,unmappedfolder,name,mappedfolder,name,mappedfolder,name,i), shell=True).wait() #out=mapped/%s.sam && samtools view -bSh1 mapped/%s.sam | samtools sort -m 80G -@ 3 -o mapped/%s_sorted.bam && samtools index mapped/%s_sorted.bam && rm mapped/%s.sam " %(ref,name,name,i,name,name,name,name,name)
		
