#!/usr/bin/env python

import sys

f=open(sys.argv[1],'r')

h=open(sys.argv[2],'r')

g=open(sys.argv[3],'w')


data={}
genera=[]
print "loading names db"
c=0
for i in h:
	c=c+1
	
	#i=i.replace('"','')
	#i=i.replace(";","\t")
	
	k= i.split("\t")
	
	genus=k[2].split(" ")[0]
	try:
		spp=k[2].split(" ")[1]
	except:
		spp="no species name"
	common=k[1]
	
	if genus not in data.keys():
		data[genus]={}
		if spp not in data[genus].keys():
			data[genus][spp]=[]
			data[genus][spp].append(common)
		else:
			data[genus][spp].append(common)
	else:
		if spp not in data[genus].keys():
			data[genus][spp]=[]
			data[genus][spp].append(common)
		else:
			data[genus][spp].append(common)
	
	
print "searching"

for i in f:

	k= i.split("\t")
	
	qgenus=k[0].split(" ")[0]
	try:
		qspp=k[0].split(" ")[1].rstrip("\n")
	except:
		qspp="no species"
	
	try:
		ans = qgenus+" "+qspp+";"+";".join(str(p) for p in data[qgenus][qspp])+"\n"
		
	except:
		if qgenus in data.keys():
		
			if qspp not in data[qgenus]:
			
				ans = qgenus+" "+qspp+"\t;no spp found"+";"+";".join(str(p) for p in data[qgenus])+"\n"
				
		else:
		
			ans = ans = qgenus+" "+qspp+"\tno genus found"+"\n"
		
	g.write(ans)
		
		
	









	