#!/usr/bin/python
import sys
import scipy.stats as sp

f=open(sys.argv[1],'r')

g=open(sys.argv[2],'w')

thresh = float(sys.argv[3])

x=f.readline() #ignore first row

names=[]
for i in f:
	names.append(i.split("\t")[0]) #NB first row of names has no tab at start

f.seek(0)
x=f.readline() #ignore first row

len1=len(names)

data={}

for i in f:
	k=i.rstrip("\n").split("\t")
	
	data[k[0]]=[]
	for p in k[1:]:
		data[k[0]].append(float(p))
		
g.write('gene1\tgene2\tR\tp\n')
c=0
t=0
for i in names:
	c=c+1
	for j in range(c,len1):
		r=sp.pearsonr(data[i],data[names[j]])
		
		#print i+"\t"+names[j]+"\t"+str(r[0])+"\t"+str(r[1])+"\n"
		#raw_input()
		
		if r[0] < -thresh or r[0] > thresh:
			t=t+1
			g.write(i+"\t"+names[j]+"\t"+str(r[0])+"\t"+str(r[1])+"\n")
	
print 'done',t,'interactions'
	
	
	
	
	
	
	
	
	
	


