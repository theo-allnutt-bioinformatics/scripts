#!/usr/bin/python
from __future__ import print_function
import sys
from Bio import SeqIO
import glob
import re

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

				  
f = open(sys.argv[1],'r') # genome fasta
h= open(sys.argv[2],'r') #gff

g=open(sys.argv[3],'w')#output fasta

print('reading reference fasta')
refseq=SeqIO.to_dict(SeqIO.parse(f,'fasta'))#,lambda rec : str(rec.id).split(" ")[0]
#print (refseq.keys())
genes={}
exons={}
contigs=[]
print('parsing gff')
for x in h:

	if x[0]<>"#":     #or x[0]<>"@"
	
		k=x.split("\t")
		contig=k[0]
		type=k[2]
		s=int(k[3])
		e=int(k[4])
		pos=(s,e)
		name=k[-1].split("Name=")[0].split(";")[0].split("-")[0] #nb '-' is delimiter between parent id and 'exon name' so has to be split
		info=k[-1].rstrip("\n")
		id=k[-1].split("ID=")[1].split(";")[0].split("-RA")[0]
		
		
		if type =="gene": #gene dict to get gene info 
			if contig not in genes.keys():
				genes[contig]={}
				genes[contig][id]=info
			else:
				genes[contig][id]=info
			
		if type=="exon":
			
			if contig not in exons.keys():
				contigs.append(contig)
				exons[contig]=[]
				exons[contig]=[("START",(0,0))]
				exons[contig].append((id,pos))
			else:
				exons[contig].append((id,pos))
		
#sort exons 
print('sorting exons')
for x in exons.keys(): #contigs
	
	exons[x].sort(key=lambda p: p[1][0])	

contigs.sort(key=tokenize)
		
#print (exons)
		
#loop exons and output intergene and genes and introns	
print('splitting fasta')
for i in contigs:
	
	conlen=len(str(refseq[i].seq))-1
	c=1
	lenexons=len(exons[i])
	
	while c<lenexons: #loop until last exon
	
		name0= exons[i][c-1][0]
		name1 = exons[i][c][0]
		
		st0=exons[i][c-1][1][0]
		en0=exons[i][c-1][1][1]
		st1=exons[i][c][1][0]
		en1=exons[i][c][1][1]
		
		#write intergenic
		if name1<>name0: #and name0<>"START":
			g.write(">"+i+";intergenic;"+name0+"--"+name1+";"+str(en0)+"--"+str(st1)+"\n"+str(refseq[i].seq[en0:st1])+"\n")
		
		#write intron
		if name1==name0: 
			g.write(">"+i+";intron;"+name0+"--"+name1+";"+str(en0)+"--"+str(st1)+"\n"+str(refseq[i].seq[en0:st1])+"\n")
		
		#write exon	
		g.write(">"+i+";exon;"+name1+";"+str(st1)+"--"+str(en1)+"\n"+str(refseq[i].seq[st1:en1])+"\n")
	
		#write end intergenic
		if c==lenexons-1 and en1<=conlen:
			print(i,'end',en1,'-',conlen)
			g.write(">"+i+";intergenic-end;"+name1+"--end;"+str(en1)+"--"+str(conlen)+"\n"+str(refseq[i].seq[en1:conlen])+"\n")
		
		c=c+1
		
		
		
		
		
		
		
		
		