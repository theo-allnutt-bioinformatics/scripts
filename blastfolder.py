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
parser.add_option("-r", "--ref", dest="subject_ref", help="subject ")
parser.add_option("-e", "--eval", dest="eval1", help="threshold e-value", default="100")
parser.add_option("-t", "--type", dest="type", help="blast type: blastn, blastp, blastx", default="blastn")
#parser.add_option("--hsps", dest="hsps", help="number of hsps to show", default="100")

(options, args) = parser.parse_args()

folder = options.infolder #sys.argv[1] #ref genome blasts folder

filelist=glob.glob(folder+"/*")

filelist.sort(key=tokenize)

subject = options.subject_ref #sys.argv[2] #ref genome to blast against

outputfolder= options.outfolder   #sys.argv[3]

if outputfolder=="":
	outputfolder="blasted"
	subprocess.check_output("mkdir -p blasted",shell=True)
else:
	subprocess.check_output("mkdir -p %s" %outputfolder,shell=True)

evalue=options.eval1
type=options.type
#hsps = options.hsps

print folder
print subject
print outputfolder
print evalue
print type

#p2 = subprocess.Popen("mkdir %s" %(outputfolder), shell=True).wait() 

for f in filelist:
	#print f
	#infile=open(f,'r')
	outname = outputfolder+"/"+f.split("/")[-1]+".blast"
	print outname, "blast parameters: task= %s evalue= %s" %(type,evalue)
	
	if type == "blastp":
		p1= subprocess.Popen("blastp -query %s -subject %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s " %(f,subject,outname,evalue), shell=True).wait() 

	if type == "blastn":
		p1= subprocess.Popen("blastn -task blastn -query %s -subject %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s " %(f,subject,outname,evalue), shell=True).wait() 
		
	if type == "blastx":
		p1= subprocess.Popen("blastx -query %s -subject %s -out %s -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore stitle' -evalue %s " %(f,subject,outname,evalue), shell=True).wait() 
		
		
		
		
		
		
		