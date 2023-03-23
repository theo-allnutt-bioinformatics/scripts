#!/usr/bin/env python3

import sys
import concurrent.futures

#r17
#used to get-seqs from large hifi files that have been split by:
#split -l 1743934 pacbio/m64134_210903_165849.hifi_reads.fastq hifi-split/hifi.fastq.

#get-seqs-para.py seqs.list "hifi-split/*.fastq" cp-reads/ 1 #can increase threads if enough mem.

def fasta2dict(f):
	data={}
	c=0
	for i in f:
		if i[0]==">":
			id1=i[1:].split(" ")[0]
			if id1 in data.keys():
				c=c+1
				id1=id1+"_"+c
			data[id1]=""
		else:
			data[id1]=data[id1]+i
	return data
	
def fastq2dict(f):
	data={}
	c=0
	n=0
	i=f.readline
	#n.b. quality can start with "@" so fetch the first few chrs of first header to use as id
	header=i[:4]
	f.seek(0)
	
	for i in f:
	
		if i[:4]==header:
			n=0
			id1=i[1:].split(" ")[0]
			if id1 in data.keys():
				c=c+1
				id1=id1+"_"+c
			data[id1]={}
			data[id1]['seq']=""
			
		elif i[0]!="+" and n==0:
			data[id1]['seq']=data[id1]['seq']+i
		elif i[0]=="+" and n==0:
			n=1
			data[id1]['qual']=""
		elif i[0]!="+" and n==1:
			data[id1]['qual']=data[id1]['qual']+i
			
	return data
			

def getseqs(i)

	outname=i.split("/")[-1]
	
	f=open(i,'r')
	
	g=open(outfolder+"/"+outname,'w')

	print('reading file',i)
	
	if ext[-1]=="a":
		fasta2dict(f)
		
	if ext[-1]=="q":
		fastq2dict(f)

	c=0
	print('fetching sequences')
	for k in listfile1:
		name1=k.rstrip("\n")
		
		if ext[-1]=="a":
		
			try:
				c=c+1
				SeqIO.write(x[name1],g,'fasta')
				print(c,name1)
			except:
				
				print(name1,'not found')

		if ext[-1]=="q":
		
			try:
				c=c+1
				SeqIO.write(x[name1],g,'fastq')
				print(c,name1)
			except:
				
				print(name1,'not found')			
		


	print("%s got %s sequences" %(str(sys.argv[2]),str(c)))

	g.close()
	f.close()

#global

print("n.b. '>' is not included in the name list to search")

listfile1 = open(sys.argv[1],'r') 

infolder = sys.argv[2] 

outfolder=sys.argv[3]

threads=int(sys.argv[4])

ext=sys.argv[2].split("/")[-1].split(".")[-1]

filelist=glob.glob(infolder)


if __name__ == '__main__':
		
	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(getseqs,i) for i in filelist]
	concurrent.futures.wait(futures1)