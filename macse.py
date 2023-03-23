#!/usr/bin/env python3
import sys
import subprocess as sp
import multiprocessing
import concurrent.futures
import os


#run macse on folders


def macse(i):
	
	print(i)
	
	f=open(infolder+"/"+i,'r')
	
	name1=i.split("/")[-1].split(".")[0].split("_")[0]

	
	p1=sp.Popen(f"java -jar /g/data/nm31/bin/macse.jar -prog alignSequences -seq {infolder}/{i} -out_NT {outfolder}/{name1}.fna",shell=True).wait()

	#-out_AA {outfolder}/{name1}.faa

	input()

	f.close()

infolder=sys.argv[1]
filelist=os.listdir(infolder)

outfolder=sys.argv[2]

threads=int(sys.argv[3])

p0=sp.Popen(f"mkdir -p {outfolder}",shell=True).wait()

if __name__ == '__main__':


	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(macse,i) for i in filelist]
	concurrent.futures.wait(futures1)
	
	#for i in filelist:
	
		#macse(i)
	
	#print("done")