#!/usr/bin/python
from Bio import SeqIO
import os
import re
import glob
import sys
import numpy
digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  
#get details on all seqs in a folder (with specified extension_

folder = sys.argv[1] #working folder

fmt = sys.argv[2]

if fmt=="fa" or fmt=="fna":
	fmt="fasta"
if fmt=="fq":
	fmt="fastq"
if fmt=="gbk":
	fmt="genbank"

print 'format:', fmt

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist
print ""
ml=max(len(w.split("/")[-1]) for w in filelist)

print "File"+(" "*(ml-4))+"\tCount"+"\tTotal_bp"+"\tMax"+"\tMin"+"\tN50"+"\tMean"
for f in filelist:

	seqs = SeqIO.index(f,fmt)
	if len(seqs)<>0:
		#get lengths and names
		data={}
		total=0
		t=0
		for i in seqs:
			t=t+1
			l1=len(seqs[i])
			
			total=total+l1
			data[i]=l1


		keylist=sorted(data,key=data.__getitem__)
		sizes=[]
		for p in keylist:
			sizes.append(data[p])
		l2=0
		min1= int(min(sizes))
		max1= int(max(sizes))
		ave=int(numpy.mean(sizes))
		for k in reversed(keylist):
			#print data[k]
			l2=l2+int(data[k])
			
			if l2>=int(total)/2:
				
				n50=int(data[k])
				break
	else:
		t=0
		total=0
		max1=0
		min1=0
		n50=0
		ave=0
	
	
	print  f.split("/")[-1]+"\t"+str(t)+"\t"+str(total)+"\t\t"+str(max1)+"\t"+str(min1)+"\t"+str(n50)+"\t"+str(ave)



