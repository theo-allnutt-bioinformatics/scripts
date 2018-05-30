#!/usr/bin/env python

import sys
import operator

#Theo Allnutt 2016
#This script opens a usearch otu table output and parses the taxonomy column (last column)
#to extract each taxonomy level separately. Levels are denoted by d:,p:,c:,o:,f:,g: before the name.
#input file is e.g. otutab.txt from:
#usearch -usearch_global trimmed.fa -db otus_tax.fa -strand both -id 0.97 -otutabout otutab.txt -biomout otutab.biom 
#usage:
#python tax_level.py otu_table.txt

#output tables are made in the current directory with -p, -c, -o, -f, -g suffixes

def find1(a,b):
	for p in a:
		if b in p:
			return a.index(p)
			
		

f = open(sys.argv[1],'r')

taxcols=int(sys.argv[2])

name1=sys.argv[1].split("/")[-1].split(".")[0]

g=open(name1+"-tax.txt",'w')

name1 = sys.argv[1].split("/")[-1].split(".")[0]
print name1


#n.b. taxa = d:,p:,c:,o:,f:,g:,s:


samples=[]

for i in f:
	if i[0]=="#":
		samples=i.split("\t")[1:]
		n=len(samples)-1
		
	else:
		break


levels=["p:","c:","o:","f:","g:","s:"]

for level in levels:
	data={}
	
	f.seek(0)
	for i in f:
		
		if i[0]<>"#":
		
			k = i.split("\t")[1:-taxcols]
			c=-1
			for x in k: #convert decimals into integers
				c=c+1
				x=int(x.split(".")[0])
				k[c]=x
			
		
			tax = i.split("\t")[-1].split(",")
			tax[-1]=tax[-1].rstrip("\n") #remove return from last taxl in list
		
			pos=find1(tax,level)
			#print pos, tax, level
			#raw_input()
			
			
			if pos is not None:
				#print 'pos',pos
				name=tax[pos].split(":")[-1]
				
				if name not in data.keys():
					
					data[name]=k
					
				else:
					for x in range(0,len(k)):
						data[name][x]=data[name][x]+k[x]
					
			else:
				
			#add to unclassified
				if "unclassified" in data.keys():
					for x in range(0,len(k)):
						
						data["unclassified"][x]=data["unclassified"][x]+k[x]
						
				else:
					data["unclassified"]=k
	
			#print level, tax,pos,k
	#print data
	#print "unclassified", data["unclassified"]
	
	#g=open(name1+"-"+level[0]+".txt",'w') # to give separate files for each tax level
	
	
	g.write(level+"\t"+"\t".join(str(x) for x in samples[:-taxcols])+"\t"+"sum"+"\n")
	
	data_sums={}
	sorted_taxa=[]
	#sort by abundance
	for i in data.keys():
		data_sums[i]=sum(data[i])
	
	sorted_taxa = sorted(data_sums.items(), key=operator.itemgetter(1))	
	print sorted_taxa
	
	for v in sorted_taxa: #data.keys():
		i=v[0]
		print i
		g.write(i+"\t"+"\t".join(str(x) for x in data[i])+"\t")
		sum1=0
		for s in data[i]:
			sum1=sum1+float(s)
		g.write(str(sum1)+"\n")
	
	g.write("\n")