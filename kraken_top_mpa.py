#!/usr/bin/env python3

#r3.3
#get highest count taxon from kraken report
#may need to rename the _all_ output to .tab1 so it aovids this file.

import sys
import re
import glob
import subprocess
import os


def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token for token, match in ((fragment, digits.search(fragment)) for fragment in digits.split(filename)))


def tophit(infolder,outfile):

	filelist=glob.glob(infolder)
	filelist.sort(key=tokenize)
	
	taxlevels=["d","k","p","c","o","f","g","s"]
	
	outfile.write("sample\tD\tK\tP\tC\tO\tF\tG\tS\tD\tK\tP\tC\tO\tF\tG\tS\n")
	
	for i in filelist:
	
		sample=i.split("/")[-1].split(".")[0]
		outfile.write(sample+"\t")
		outline=["","","","","","","",""]
		outcounts=[0,0,0,0,0,0,0,0]
		
		print(i)
		f=open(i,'r')
		c=0
		n=0
		
		taxtot={}
		levcounts={}
		for p in taxlevels:
			levcounts[p]={}
		
		for x in f:
		
			k=x.rstrip("\n").split("|")
			lev=k[-1].split("__")[0]
			levname=k[-1].split("__")[1].split("\t")[0]
			num=int(k[-1].split("\t")[1])
			
			if lev not in taxtot.keys():
				taxtot[lev]=num
			else:
				taxtot[lev]=taxtot[lev]+num
		
			if levname not in levcounts[lev].keys():
				levcounts[lev][levname]=num
			else:
				levcounts[lev][levname]=levcounts[lev][levname]+num #n.b. this should not happen becuase should only be one entry at root of each level
				
			
		#save pie chart data for each tax level.
		
		g2=open(f"{sample}_tax_counts.tab",'w')
		
		for v in taxlevels:
		
			g2.write(v)
			
			taxnames=[]
			for w in levcounts[v].keys():
				taxnames.append((w,levcounts[v][w]))
			
			taxnames.sort(key=lambda z: z[1])
			
			for x in taxnames:
				g2.write("\t"+x[0])
			g2.write("\n")
			g2.write(sample)
			for y in taxnames:
				g2.write("\t"+str(y[1]))
			g2.write("\n\n")
			
		g2.close()
			
			
			
		
		f.seek(0)
		
		for x in f:

			k=x.rstrip("\n").split("|")
			
			nreads=k[-1].split("\t")[1]
			
			tax=k[-1].split("__")[0]
			name=k[-1].split("__")[1].split("\t")[0]
			
			if taxlevels.index(tax)==c: #check if taxlevel increasing.. if not stop and write
				outline[taxlevels.index(tax)]=name
				outcounts[taxlevels.index(tax)]=nreads
				c=c+1
			else:
				outfile.write("\t".join(str(v) for v in outline)+"\t"+"\t".join(str(v) for v in outcounts)+"\n")
				n=1
				break
		if n==0:
			outfile.write("\t".join(str(v) for v in outline)+"\t"+"\t".join(str(v) for v in outcounts)+"\n")
		
		
		
		
def main():

	infolder = sys.argv[1] #result folder
	outfile = open(sys.argv[2],'w') 

	tophit(infolder, outfile)

	print("done")
	
	

if __name__ == '__main__': main()


	
		
		
		
		