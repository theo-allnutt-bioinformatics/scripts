#!/usr/bin/env python3

#from R02.2 get nanopore reads from minimap .sam file that overlap numpts from gff3 file. Cannot extract secondary or soft clipped lengths.

import sys

f = open(sys.argv[1],'r') #input sam
h = open(sys.argv[2],'r') #gff3 file of nunmpts

g = open(sys.argv[3],'w') #sam output

overlap = int(sys.argv[4])
filename=sys.argv[1].split("/")[-1].split(".")[0]

e = open(filename+"_summary.tab",'w')
e.write("numpt\tcontig\toverlap_reads\tnon-overlap_reads\n")

#get contig lengths
reads={}
hits=[]
contigs=[]
print("Reading sam")
for i in f: #store sam read contigs and pos in dict if mapped.. k[5]=* if unmapped
	if i[0]!="@":
		k=i.rstrip("\n").split("\t")
		id1=k[0]
		contig=str(k[2])
		cigar=str(k[5])
		if contig not in contigs and cigar!="*":
			reads[contig]={}
			contigs.append(contig)
			
		x=int(k[3]) #start position
		
		#count masked bases and subtract soft and hard clip bases from seq length
		
		cliplen=0
		digits1=""
		
		for j in cigar:
			if j.isdigit():
				digits1=digits1+j #make a string of any digits
						
			elif j=="S" or j=="H": #soft and hard clip codes go after the number of bases digits
				cliplen=cliplen+int(digits1)
				digits1=""
				
			if j=="M" or j=="I" or j=="=" or j=="X" or j=="D": #if digits were for any other code then reset digits
				digits1=""
							
		y = int(len(k[9])-cliplen+x) #end positition
		
		#if x<y: #not needed for sam, x always leftmost
		if cigar!="*":
			reads[contig][id1]=(x,y,i)
		#else:
			#reads[contig][id1]=(y,x,i)

numpt={}
c=0
for i in h: #search gff against reads for overlaps
	c=c+1
	
	k=i.rstrip("\n").split("\t")
	contig=str(k[0])
	
	numptid=i.split("ID=")[1].split(";")[0].rstrip("\n")
	
	print("numpt",numptid,"contig",contig,end=" "),
	
	e.write(numptid+"\t"+contig+"\t")
	
	x=int(k[3])
	y = int(k[4])
	
	if x<y:
		start=x
		end=y
	else:
		start=y
		end=x
	n=0 #overlap reads
	p=0 #non-overlap reads
	if contig in contigs:
		for j in reads[contig].keys():
			readx=reads[contig][j][0]
			ready=reads[contig][j][1]
			
			if  (readx < start - overlap and ready > start + overlap) or (readx < end - overlap and ready > end +overlap):
				n=n+1
				g.write(reads[contig][j][2]) #write sam line for read to output
			
			if  (readx >= start - overlap and ready < end + overlap):
				p=p+1
				g.write(reads[contig][j][2]) #write sam line for read to output n.b. did not previously write these non-overlap reads but it is useful to see them
				
				
		print(n,"overlap reads",p,"internal reads")
		e.write(str(n)+"\t"+str(p)+"\n")
		
	else:
		e.write("0\t0\n")	
print("done - can close manually - python may take some time to close automatically")		
		
e.close()
f.close()
g.close()
h.close()
	
		
		
		
		
		