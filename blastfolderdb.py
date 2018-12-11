#!/usr/bin/python
import sys
import re
import glob
import subprocess
from optparse import OptionParser

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

parser = OptionParser()
parser.add_option("-i", "--infolder", dest="infolder", default="./",help="input sequence folder", metavar="FILE")
parser.add_option("-o", "--outfolder", dest="outfolder", default="./", help="output folder")
parser.add_option("-r", "--ref", dest="subject_ref", help="subject database")
parser.add_option("-e", "--eval", dest="eval1", help="threshold e-value", default="100")
parser.add_option("-t", "--type", dest="type", help="blast type: blastn, blastp, blastx, tblastx, tblastn", default="blastn")
parser.add_option("--hsps", dest="hsps", help="number of hsps to show", default="1000")
parser.add_option("--threads", dest="threads", help="number of threads to use", default="4")
#parser.add_option("-m", "--max_seqs", dest="maxs", default="100",help="max number of target seqs")
#removed due to bad behavior, use max_hsps only

(options, args) = parser.parse_args()

folder = options.infolder #sys.argv[1] #ref genome blasts folder

filelist=glob.glob(folder)

filelist.sort(key=tokenize)

subject = options.subject_ref #sys.argv[2] #ref genome to blast against

outputfolder= options.outfolder   #sys.argv[3]
threads = options.threads

evalue=options.eval1
type=options.type

hsps = options.hsps
#maxs = options.maxs

print folder
print subject
print outputfolder
print evalue
print type
print filelist
#p2 = subprocess.Popen("mkdir %s" %(outputfolder), shell=True).wait() 
c=-1
p1=[""]*int(threads)
for f in filelist:
	c=c+1
	
	print 'thread',c
	
	outname = outputfolder+"/"+f.split("/")[-1]+".blast"
	print outname, "blast parameters: task= %s evalue= %s" %(type,evalue)
	
	if type == "remote":
	
		print "blastn -remote -query %s -db nt -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s  -max_hsps %s " %(f,outname,evalue,hsps)
		
		p1[c]= subprocess.Popen("blastn -remote -query %s -db nt -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s  -max_hsps %s " %(f,outname,evalue,hsps,), shell=True) 
	
	if type == "blastp":
		p1[c]= subprocess.Popen("blastp -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s -num_threads 24 -max_hsps %s" %(f,subject,outname,evalue,hsps), shell=True)

	if type == "blastn":
		p1[c]= subprocess.Popen("blastn -task blastn -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s -num_threads 24 -max_hsps %s" %(f,subject,outname,evalue,hsps), shell=True) 
		
	if type == "blastx":
		p1[c]= subprocess.Popen("blastx -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s -num_threads 24 -max_hsps %s" %(f,subject,outname,evalue,hsps), shell=True)
		
	if type == "tblastx":
		p1[c]= subprocess.Popen("tblastx -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s -num_threads 24 -max_hsps %s" %(f,subject,outname,evalue,hsps), shell=True)
		
	if type == "tblastn":
		p1[c]= subprocess.Popen("tblastn -query %s -db %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s -num_threads 24 -max_hsps %s" %(f,subject,outname,evalue,hsps), shell=True)
		
	if c>=int(threads)-1:
		for v in range(c):
			p1[v].wait()
		c=-1

if type == "remote":		
	print 're-running on db error files for remote type. may require manual stop.'
	nohits=1
	
	while nohits==1:
		n=0
		for f in filelist:
			c=c+1
		
			print 'thread',c
			h=open(outputfolder+"/"+f+".blast",'r')
			if h.readline()[0]=="":
				n=n+1
				h.close()
				
				outname = outputfolder+"/"+f.split("/")[-1]+".blast"
				print outname, "blast parameters: task= %s evalue= %s" %(type,evalue)
				
				print "blastn -remote -query %s -db nt -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s  -max_hsps %s" %(f,outname,evalue,hsps)
				
				p1[c]= subprocess.Popen("blastn -remote -query %s -db nt -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s  -max_hsps %s" %(f,outname,evalue,hsps), shell=True) 
				
				
			if c>=int(threads)-1:
				for v in range(c):
					p1[v].wait()
				c=-1
		if n==0:
			nohits=0
		
		
		
		
		
