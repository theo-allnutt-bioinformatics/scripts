#!/usr/bin/env python3
import sys
import re
import glob
import subprocess
import multiprocessing
import concurrent.futures



digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

def fastp_paired(file1,file2,outfolder,keep_len,fpt):


	out1=outfolder+"/"+file1.split("/")[-1]
	out2=outfolder+"/"+file2.split("/")[-1]
	print(out1,out2)
	p1=subprocess.Popen("fastp -i %s -I %s -o %s -O %s -g -l %s -w %s -y -Y 60" %(file1,file2,out1,out2,keep_len,fpt),shell=True).wait()

				
def fastp_single(file1,outfolder,keep_len,fpt):
	
	out1=outfolder+"/"+file1.split("/")[-1]
	print(out1)
	p1=subprocess.Popen("fastp -i %s -o %s -g -l %s -w %s -y -Y 60" %(file1,out1,keep_len,fpt),shell=True).wait()
			

def main():

	folder = sys.argv[1] 

	filelist=glob.glob(folder)

	filelist.sort(key=tokenize)
	print(filelist)

	outfolder=sys.argv[2]

	keep_len=sys.argv[3]

	threads=int(sys.argv[4])
	
	fpt = sys.argv[5] #threads per fastp
	
	paired=sys.argv[6]

	#fastp(filelist,outfolder,keep_len,paired)

	p0=subprocess.Popen("mkdir -p %s" %outfolder,shell=True).wait()

	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	
	if paired=="paired":
	
		futures1 = [executor1.submit(fastp_paired,filelist[i],filelist[i+1],outfolder,keep_len,fpt) for i in range(0,len(filelist)-1,2)]
		concurrent.futures.wait(futures1)	

		print("done")
		
	if paired=="single":
	
		futures1 = [executor1.submit(fastp_single, i,outfolder,keep_len,fpt) for i in filelist]
		concurrent.futures.wait(futures1)	

		#print("done")
	
		#for i in filelist:
		
			#fastp_single(i,outfolder,keep_len,fpt)

if __name__ == '__main__': main()