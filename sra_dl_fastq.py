#!/usr/bin/env python3

import sys
import re
import glob
import subprocess as sp
from Bio import Entrez
#from datetime import date
import os.path
#import concurrent.futures

#dl sra fastqs
#written for r3.21
#Theo Allnutt 2022
#Thanks to https://edwards.flinders.edu.au/fastq-dump/
#usage
#sra_dl_fastq.py search_terms.txt sra_fastq/ 24 


#n.b. can also use fastq-dump if only a range is to be downloaded. fastq-dump is actually just as fast.
#fastq-dump -N 10000 -X 50010000 --outdir reads-temp --skip-technical  --readids --read-filter pass --dumpbase --split-3 --clip SRR2912886


Entrez.email = "theodore.allnutt@rbg.vic.gov.au"

Entrez.api_key = "8c29872371a4c4de3fdc0c6570e15625ba08"


def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment))for fragment in digits.split(filename)))


def get_records(i,threads,outfolder):


	q=i.rstrip("\n")
		
	try:
		print(i)
		p1=sp.Popen("fasterq-dump -p --outdir fastq -S --threads %s --skip-technical %s" %(threads,q),shell=True).wait()
		
		p2=sp.Popen("mv fastq/%s*.fastq %s/ " %(q,outfolder),shell=True)
	except:
		
		print(i,'download failed')
			

	
def main():

	f=open(sys.argv[1],'r')
	outfolder=sys.argv[2]
	threads=sys.argv[3]
	sp.Popen('mkdir -p %s' %outfolder,shell=True).wait()
	
	


	for i in f:
		get_records(i,threads,outfolder)


if __name__ == '__main__': main()


		