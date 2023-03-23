#!/usr/bin/env python3


import sys
import os
import re
import glob


def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))



def concat_parts(filelist):
	
	for x in range(0,len(filelist),2):
		
		name1=filelist[x].split("/")[-1]
		rootname=".".join(str(p) for p in name1.split(".")[:-1])
		
		f1=open(filelist[x],'r')
		f2=open(filelist[x+1],'r')
		
		print(filelist[x],filelist[x+1])
		
		r1=f1.readlines()    
		r2=f2.readlines()  
		
		f1.close()
		f2.close()
		
		
		#trim to nearest whole 4 lines
		c1=float(len(r1)/4)
		d1=int(str(c1).split(".")[0])
		
		c2=float(len(r2)/4)
		d2=int(str(c2).split(".")[0])
		
		print(d1,d2)
		
		if d1<d2:
			nlines=d1
		else:
			nlines=d2
			
		#check last qual line is complete, if not, go back four lines
		if len(r1[nlines])!=len(r1[nlines-2]) or len(r2[nlines])!=len(r2[nlines-2]):
			nlines=nlines-4
			print("incomplete quality line, nlines=",nlines)
			
		
		#write trimmed r1 and r2 
		print("writing")
		g1=open(outfolder+"/"+rootname+"_R1.fastq",'w')
		g2=open(outfolder+"/"+rootname+"_R2.fastq",'w')
		
		c=0
		
		while c<nlines:
		
			id1=r1[c].split(" ")[0]
			id2=r2[c].split(" ")[0]
			
			seq1=r1[c+1]
			qual1=r1[c+3]
			
			seq2=r2[c+1]
			qual2=r2[c+3]
			
			g1.write(f"{id1}\n{seq1}+\n{qual1}")
			g2.write(f"{id2}\n{seq2}+\n{qual2}")
			
			c=c+4
		
		g1.close()
		g2.close()
		

#global

folder=sys.argv[1] 
filelist=glob.glob(folder)
filelist.sort(key=tokenize)
print("files",filelist)
outfolder = sys.argv[2] #outfolder


if __name__ == '__main__':
	
	concat_parts(filelist)




		