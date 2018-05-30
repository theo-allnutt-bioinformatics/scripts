#!/usr/bin/python

import sys


f=open(sys.argv[1],'r')

h=open(sys.argv[2],'r')

g=open(sys.argv[3],'w')

level=sys.argv[4]



samples=f.readline().rstrip("\n").split("\t")[1:]


#get habitat data
habitat={}
for j in h:

	sp=j.split("\t")[0]
	
	hab = j.rstrip("\n").split("\t")[1]

	habitat[sp]=hab

def genus(habitat,samples,f):

	genhabs={}
	
	for i in habitat.keys():
		
		k = i.split("_")[0]
		hab= habitat[i]
		
		if k not in genhabs.keys():
		
			genhabs[k]=[]
			genhabs[k].append(hab)
			
		else:
		
			genhabs[k].append(hab)
			
	#print genhabs
	genprops={}
	for i in genhabs.keys():
		
		genprops[i]={}
			
		for j in list(set(genhabs[i])):
				
			prop=float(genhabs[i].count(j))/float(len(genhabs[i])) #get proportion of habitat in list
				
			genprops[i][j]=prop
				
	#print genprops
	
	data={}
	for i in f:

		gen=i.split("_")[0]
		
		line=i.rstrip("\n").split("\t")
		
		if gen in genprops.keys():
			hab=genprops[gen]
			print gen, hab
			
			for j in hab.keys():
			
			
				if j not in data.keys():
			
					data[j]=[]
				
					for x in line[1:]:
				
						data[j].append(float(x)*hab[j])
					
				else:
					c=-1
					for x in line[1:]:
						c=c+1
						data[j][c]=data[j][c]+(float(x)*hab[j])
		
		
		
		else:
			hab="unknown"
			if hab not in data.keys():
				
				data[hab]=[]
				
				for x in line[1:]:
				
					data[hab].append(float(x))
					
			else:
				c=-1
				for x in line[1:]:
					c=c+1
					data[hab][c]=data[hab][c]+int(float(x))		
					
					
	return data
	
	
	
	
	
	
#read otu table and get habitats
def species(habitat,f):
	data={}
	for i in f:

		sp=i.split("\t")[0]
		
		line=i.rstrip("\n").split("\t")
		
		if sp in habitat.keys():
			hab=habitat[sp]
			print sp, hab
			if hab not in data.keys():
			
				data[hab]=[]
				
				for x in line[1:]:
				
					data[hab].append(int(float(x)))
					
			else:
				c=-1
				for x in line[1:]:
					c=c+1
					data[hab][c]=data[hab][c]+int(float(x))
		else:
			hab="unknown"
			print sp,hab
			if hab not in data.keys():
				
				data[hab]=[]
				
				for x in line[1:]:
				
					data[hab].append(int(float(x)))
					
			else:
				c=-1
				for x in line[1:]:
					c=c+1
					data[hab][c]=data[hab][c]+int(float(x))		
					
					
	return data
if level=="species":	
	output=species(habitat,f)
	
elif level=="genus":
	output=genus(habitat,samples,f)
	
else:
	print "enter species or genus as taxonomic level"
	
title="habitat\t"+"\t".join(str(p) for p in samples)

g.write(title+"\n")

for i in output.keys():

	output2 = "\t".join(str(p) for p in output[i])
	
	g.write(i+"\t"+output2+"\n")

print 'Habitats found:'	
print output.keys()
		
			
			
