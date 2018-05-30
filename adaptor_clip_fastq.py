#!/home/theoa/qiime-env/env/bin/python

#Theo Allnutt 2018


import sys
import subprocess
from Bio import SeqIO
from fuzzysearch import find_near_matches



f = open(sys.argv[1],'r')
g = open(sys.argv[2],'w')
rightp = sys.argv[3].upper()
mm=int(sys.argv[4])
size=int(sys.argv[5])


l=0
r=0
t=0
c=0

p1=subprocess.check_output('prg %s' %rightp, shell=True).split("\n")[:-1]

	
print "adaptor to clip:",p1


#qual={}

nf=0
art=0
for x in SeqIO.parse(f,'fastq'):
	c=c+1
	t=t+1
	q1="y"
	q2="y"
	if c==10000:
		print t, "clipped=",str(r)	
		c=0
			
	for primer in p1:
		seq1=str(x.seq)
		m=find_near_matches(primer,seq1,max_l_dist=mm)
		
		if m<>[]:
			q = m[0].start #nb clip at first instance
			r=r+1
			qual=list(x.letter_annotations["phred_quality"])[:q]
			
			del x.letter_annotations["phred_quality"]
			x.seq=x.seq[:q]
			x.letter_annotations["phred_quality"]=qual
			q1="y"
			break
		else:
			q2="no hit"
				
	if len(x.seq) >size:		
		SeqIO.write(x,g,'fastq')
		
		
print str(l),"adaptors clipped"