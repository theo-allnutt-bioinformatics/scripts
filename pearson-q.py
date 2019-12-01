#!/usr/bin/env python
import sys
import scipy.stats as sp
import warnings
warnings.simplefilter('error')

#calculate pearson R between two matrices, e.g. otu table R for each OTU with metadata
#OTU table has otus in rows, sample names in first row
#metadata has sample names in first row and metadata in rows, i.e. transpose the qiime format

#outputs an otu Vs metadata table of R
#meta data must be numerical
#missing values must be NaN


f1=open(sys.argv[1],'r') #otu table, samples in columns

f2=open(sys.argv[2],'r') #transposed metadata, samples in columns

g=open(sys.argv[3],'w')

pthresh=float(sys.argv[4])

rthresh=float(sys.argv[5])

if sys.argv[1]==sys.argv[2]:
	selfmode=1
else:
	selfmode=0

otus=[]
metanames=[]
result={}
presult={}
bh=[]
print "calculating correlations"

lines1=[]
lines2=[]
f1.readline()
for i in f1:
	lines1.append(i)
	
f2.readline()
for j in f2:
	lines2.append(j)


t=0
for i in lines1:
	if selfmode==1:
		t=t+1
	k1=i.split("\t")
	k1[-1]=k1[-1].rstrip("\n")
	otu=k1[0]
	
	if otu not in otus:
		otus.append(otu)
	
	result[otu]={}
	presult[otu]={}
	#f2.readline()
	
	for j in lines2[t:]:
	
		k2=j.split("\t")
		k2[-1]=k2[-1].rstrip("\n")
		metaname=k2[0]
		#print k2
		if metaname not in metanames:
			metanames.append(metaname)
		
		x=k1[1:]
		y=k2[1:]
		c=-1
		while c< len(x):
			if x[c]=='NaN' or y[c]=='NaN':
				del x[c]
				del y[c]
			else:
				
				x[c]=float(x[c])
				y[c]=float(y[c])
				c=c+1
			
		try:
			 
			rho, pval = sp.pearsonr(x,y)
			result[otu][metaname]=(rho) #R
			presult[otu][metaname]=(pval)
			
			bh.append((otu,metaname,float(rho),float(pval)))	
			
		except:
			print 'error in pearson calculation, zero sd........................................'
			print otu
			print x
			print metaname
			print y
			result[otu][metaname]=0 #R
			presult[otu][metaname]=1

	
g.write("source\ttarget\tR\tp-value\tbhq\n")

numt = float(len(otus)*len(metanames))
print 'total correlations=',numt

#Benjamini-Hochberg

bh_srt=sorted(bh,key=lambda x:x[3])
n1=0
qresult=[]
for v in bh_srt:
	n1=n1+1
	bhq= float((n1/numt)*pthresh)
	qresult.append((v[0],v[1],v[2],v[3],bhq)) #otu, metaname, R, pval, bhq



c=0
highq=0
for i in qresult:
	c=c+1
	if i[3]<i[4]:
		highq=c
c=0
if highq<>0:

	for j in range(highq):
		k=qresult[j]
		otuout=k[0]
		metout=k[1]
		Rout=str(k[2])
		pout=str(k[3])
		qout=str(k[4])
		#print otuout, metout, Rout, pout, qout
		
		if float(Rout)>=rthresh or float(Rout)<= -rthresh:
			
			if selfmode==1:
				if otuout<>metout:
					c=c+1
					g.write(otuout+"\t"+metout+"\t"+Rout+"\t"+pout+"\t"+qout+"\n")
			else:
				c=c+1
				g.write(otuout+"\t"+metout+"\t"+Rout+"\t"+pout+"\t"+qout+"\n")

	print c,'correlations with bhq <',pthresh,'and R<>',rthresh
				
else:
	print "No signficant (B-H P<=%s) correlations found" %pthresh
			
			
			
			


	

	


	
	
	
	
	


