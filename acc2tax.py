#!/usr/bin/env python

import sys
import os
import subprocess
import re
import glob
from random import randrange

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))
				  

#made in project 075.10

#taxonfetch.py theo allnutt 2019. Gets the taxonomy ID number from a local copy of the NCBI GI/taxonomy list file #and retrieves the scientific lineage field from nodes and names file using tax_trace.pl. ID and lineage are then appended to the end of the submitted #blast output (tab format, 6) file.

#this software has no guarantees of working or doing anything and should not be used for anything.


 #tab format blast output (6) Sequence accessions (hits) in second column
 #taxa are added to end columns - name of appended file
taxaid = sys.argv[2] #sorted and reduced version of ncbi nucl_wgs.accession2taxid file
#n.b. to make the taxdb:
#sort nucl_wgs.accession2taxid > sorted.txt
#cut -f1,3 sorted.txt > acc2taxid.txt
#rm sorted,txt

folder=sys.argv[1] #ublast, acc2tax.py result file
filelist=glob.glob(folder)
filelist.sort(key=tokenize)

rarefy=int(sys.argv[3])

print filelist

print "searching.."
size = long(os.path.getsize(taxaid))

print "TaxID File Size: ", size
dbfile = open(taxaid,'r')


for file in filelist:
	print file
	
	f=open(file,'r')
	g=open(file.split(".")[0]+".tax",'w')

	c=0
	dataout = ""
	t=0
	 #get the ncbi accessions
	gi=[] #n.b. they are not GIs, just used this name from older version
	dataout=[]
	ids=[]

	r2=str(randrange(100000))
	split_place=1
	
	input_species=[]
	setgi=[]
	
	for line2 in f:
		c=c+1
		if c<rarefy:
			k=line2.split("\t")[1].split('.')[0].replace("_","")
			gi.append(k) #underscores must be removed from db file
			input_species.append(line2.split("\t")[1])
			
			if k not in setgi:
				setgi.append(k)
		else:
			break
		
	print str(c),"Accessions"
	print len(setgi),"set"
	
	c=0
	setgitax={}
	gitax=[]
	names =[]
	t=0
	############make set(gi)isntead to speed up
	
	
	for gis in setgi: #binary search of the set of gis only#########################################
		c=c+1
		#print gis
		found=False
		offset=0
		chunk=size
		pos=chunk/2
		
		while found == False and chunk>0:
			
			chunk = chunk/2
			dbfile.seek(pos)
			dbfile.readline() #has to readline first to ignore partial line seek position
			entry = dbfile.readline().split("\t")
			filegi = entry[0]
			filetax = entry[1].rstrip("\n")
			
			if filegi == gis:
				answer = filetax
				found = True
				
			elif filegi > gis: #N.B. these are operating on python ability to use numerical operators on  sorted strings
				pos = offset +(chunk/2)
			
			elif filegi < gis:
				offset = offset+chunk
				pos = pos + (chunk/2)
		
		if found == False:
			answer = "no taxonomy" #"32644"
			print c,":",gis, answer
		
		setgitax[gis]=answer
		
	#fetch taxonomy from setgitax
	
	for i in gi:
		gitax.append(setgitax[i])
	
		
	#print gitax	#list of Gi's taxids
	cc1=-1
	v1=-1
	p=""

	#save gitax to tempfile

	tmp1 = open('./%stmp1.txt' %r2,'w')

	cnt1=-1

	for i in gitax:
		cnt1=cnt1+1
		tmp1.write(str(gi[cnt1])+"\t"+str(i)+"\n")
		
	tmp1.close()

	#change this line to your location for tax_trace.pl and nodes and names and temp files
	p1=subprocess.Popen("perl ~/scripts/tax_trace.pl ~/db/nodes.dmp  ~/db/names.dmp ./%stmp1.txt ./%stmp2.txt " %(r2,r2),shell=True).wait()
		

	f.seek(0)
	#change line to temp file location
	p3=open("./%stmp2.txt" %r2,'r')
	p4=[]



	for i in p3:
		names.append(i.rstrip("\n")) #list of lineages
		
	#print "\n".join(str(x) for x in names)
	#print len(names)
	n=-1
	c=0
	for line4 in f:
		c=c+1
		if c<rarefy:
			n=n+1
			
			if len(names[n].split("\t"))==1:
				lineage=line4.rstrip('\n')
				nohitsuffix="no taxonomy found\tno rank|no rank|superkingdom|no rank|phylum|class|order|family|genus|species\troot|na|na|na|na|na|na|na|na|"+input_species[n]+"\n"
				g.write(lineage+"\t"+nohitsuffix)
				
				#input_species[n]+"\t"++"\tno taxonomy found"+"\n
				
			else:
				lineage=line4.rstrip('\n')+"\t"+gitax[n].rstrip("\n")+"\t"+names[n].split("\t")[2]+"\t"+names[n].split("\t")[3]+"\n"
				#print lineage
				g.write(lineage)	


	#change line to temp file location
	subprocess.Popen("rm -f ./%stmp1.txt" %r2,shell=True).wait()
	subprocess.Popen("rm -f ./%stmp2.txt" %r2,shell=True).wait()
	g.close()
	f.close()
