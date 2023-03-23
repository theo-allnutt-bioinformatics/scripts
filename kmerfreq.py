#!/usr/bin/env python3

#r17 finding if any  common motifs before numpts using kmer freqs

import sys
import os
import re
import glob
import subprocess as sp
import concurrent.futures
from Bio import SeqIO
import gzip
import math
import collections





def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))


def kmerfreq(dna_sequence,wordsize):
	
	wordsizeint=int(wordsize)
	kmers=[]
	seqlen=float(len(dna_sequence))
	wordsize=float(wordsize)
	

	#posscount=float((4**wordsize)*(1-math.exp(-(1/(4**wordsize))*seqlen)))
	#print(posscount)
	for x in range(len(dna_sequence)-wordsizeint):
		
		kbit=dna_sequence[x:x+wordsizeint]

		kmers.append(kbit) #also try if to test before set see which is faster: 
		

	kmerset=set(kmers)
	
	for i in kmerset:
	
		print(i,kmers.count(i))
		

	
	
infile=sys.argv[1] 

wordn=int(sys.argv[2])



if __name__ == '__main__':
	
	seq1=""
	for x in SeqIO.parse(infile,'fasta'):
		seq1=seq1+str(x.seq)
		
	
	
	kmerfreq(seq1,wordn)
	



		