#!/usr/bin/env python

#Theo Allnutt 2016
#Trims sequences to specified primers, removing the primers.
#Useage:
#primer_clip_fastq.py infile.fasta trimmed.fasta NCTAYGGGRBGCASCAG ATTAGATACCCNNGTAGTCN 2 n
#NCTAYGGGRBGCASCAG is forward primer
#ATTAGATACCCNNGTAGTCN is REVERSE COMPLEMENT of reverse primer
#'15' is the 3' length to recognise for hit
#requires 'prg.c' code (compiled and in path) for making degeneracy
#https://pypi.python.org/pypi/fuzzysearch/0.2.2 - doesn't work, freezes 
#functions from here:
#https://stackoverflow.com/questions/31365168/string-regex-two-mismatches-python 

import sys
import subprocess
from Bio import SeqIO
from fuzzysearch import find_near_matches



f = open(sys.argv[1],'r')
g = open(sys.argv[2],'w')
leftp = sys.argv[3].upper()
rightp = sys.argv[4].upper()
mm=int(sys.argv[5])
mode=sys.argv[6]

l=0
r=0
t=0
c=0

p0=subprocess.check_output('prg %s' %leftp, shell=True).split("\n")[:-1]
p1=subprocess.check_output('prg %s' %rightp, shell=True).split("\n")[:-1]
	
print "forward primer to clip:",p0
print "reverse primer to clip:",p1

#qual={}

nf=0
art=0
passed=0
for x in SeqIO.parse(f,'fastq'):
	c=c+1
	t=t+1
	q1="n" #set switch to no primer found
	q2="n"
	if c==10000:
		print t, "left clipped=",str(l),"right clipped=",str(r)	
		c=0

	for primer in p0:
		seq1=str(x.seq)
		m=find_near_matches(primer,seq1,max_l_dist=mm)
		
		if m<>[]:
			q = m[-1].end #nb clip at last instance
			#print primer,m,q
			l=l+1
			
			qual=list(x.letter_annotations["phred_quality"])[q:]
			
			del x.letter_annotations["phred_quality"]
			#print str(x.seq)
			x.seq=x.seq[q:]
			x.letter_annotations["phred_quality"]=qual
			#print str(x.seq),q
			#raw_input()
			q1="y" #set switch to primer found
			break
		else:
			q1="no hit"
			#print primer,"not found in",str(x.id)
			
	for primer in p1:
		seq1=str(x.seq)
		m=find_near_matches(primer,seq1,max_l_dist=mm)
		
		if m<>[]:
			q = m[0].start #nb clip at first instance
			r=r+1
			qual=x.letter_annotations["phred_quality"][:q]
			del x.letter_annotations["phred_quality"]
			x.seq=x.seq[:q]
			x.letter_annotations["phred_quality"]=qual
			q2="y" #set switch to primer found
			break
		else:
			q2="no hit"
			
	if q1 =="no hit" or q2 =="no hit":

		art=art+1
	
	if mode =="n" and q1=="y" and q2=="y":
		passed=passed+1
		SeqIO.write(x,g,'fastq')
		
	if mode <>"n":
		passed=passed+1
		SeqIO.write(x,g,'fastq')
		
		
print str(l),"left primers clipped",str(r),"right primers clipped"
print 'Sequences with either primer missing (artefacts) =', art 
print 'Sequences saved (passed) =',str(passed)