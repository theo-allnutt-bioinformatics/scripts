#!/usr/bin/env python3
import sys
import subprocess as sp
from Bio import SeqIO

#r17


def mapnoself(contig):
	
	p1=sp.Popen(f"minimap2 -x asm20 -t 48 ref.fasta {contig}.fasta > {contig}_c.paf",shell=True).wait()


h=open(sys.argv[1],'r')

f=open(sys.argv[2],'r')

ref = SeqIO.to_dict(SeqIO.parse(f,'fasta'))
print(ref.keys())
contigs=[]

for i in h:
	contigs.append(i.rstrip("\n"))
h.seek(0)

if __name__ == '__main__':

	for i in h:
		
		print(i)
		
		contig=i.rstrip("\n")
		
		#make contig file and ref file with no contig
		
		contigfile=open(contig+".fasta",'w')
		reffile=open("ref.fasta",'w')
		
		SeqIO.write(ref[contig],contigfile,'fasta')
		
		for x in contigs:
			if x!=contig:
			
				SeqIO.write(ref[x],reffile,'fasta')
	
		contigfile.close()
		reffile.close()

		mapnoself(contig)
	
		p0=sp.Popen(f"rm {contig}.fasta ref.fasta",shell=True).wait()
		
	p2=sp.Popen("cat *_c.paf > cat.paf",shell=True).wait()
	p3=sp.Popen("rm *_c.paf",shell=True).wait()
	
	print("plotting")
	p4=sp.Popen("pafCoordsDotPlotly.R -i cat.paf -o cat -q 100 -m 100 -p 8 -l -x -k 67",shell=True).wait()
	
	
	print("done")