#!/usr/bin/env python
#Theo Allnutt 2015
from Bio import SeqIO
import sys
import re
import glob
import statistics

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))

				  
folder = sys.argv[1] #open(sys.argv[1],'r') #open(sys.arv[1],'r')

filelist=glob.glob(folder)
filelist.sort(key=tokenize)

fmt = sys.argv[2]

bins = int(sys.argv[3])

samplesize=sys.argv[4]

#g=open(sys.argv[1]+".hist",'w')

print filelist

data=[]
for infile in filelist:
	c=0
	p=[]
	f=open(infile,'r')
	for x in SeqIO.parse(f,fmt):
		c=c+1
		
		if samplesize<>"n":
		
			if c<=int(samplesize):
			
				p.append(int(len(x.seq)))
			else:
				break
		else:
			p.append(int(len(x.seq)))
			
			
	#print p[:100]
	mean1 =statistics.mean(p)
	stdev1=float(statistics.stdev(p))
	h1=max(p)
	l1=min(p)

	step=bins#int(h1/bins)
	print "\n"
	print infile
	print "bin","Count"
	for i in range(l1,h1+step,step):

		t = sum(1 for v in p if v >= i and v < (i+step))

		print i,i+step,t
		#g.write(str(i)+"\t"+str(i+step)+"\t"+str(t)+"\n")
		data.append((i,i+step,t))
		
	print "file"+"\t\tNum\tmean\tstdev\thigh\tlow"
	print "%s\t%d\t%d\t%d\t%d\t%d\t" %(infile,c,mean1,stdev1,h1,l1)
	

#g.write("file\tNum\tmean\tstdev\thigh\tlow\n")
#g.write("%s\t%d\t%d\t%d\t%d\t%d\t" %(i,c,mean1,stdev1,h1,l1))
		






