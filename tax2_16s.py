#!/usr/bin/python
from Bio import SeqIO
import sys

'''
#reads a list of taxonomy from a file and extracts the closest taxonomy maches of fasta files from greengenes db
#usage:
#tax2_16s.py taxa.list gg_13_5.fasta gg_13_5_taxonomy.txt output16s.fasta
#taxonomy must be same format as gg, e.g. k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Enterobacterales; f__; g__; s__
#Before use, clean up the taxonomy file - remove trailing levels and square brackets
sed -i 's/\[//g' gg_13_5_taxonomy.txt
sed -i 's/\]//g' gg_13_5_taxonomy.txt
sed -i 's/ c__;//g' gg_13_5_taxonomy.txt
sed -i 's/ o__;//g' gg_13_5_taxonomy.txt
sed -i 's/ f__;//g' gg_13_5_taxonomy.txt
sed -i 's/ g__;//g' gg_13_5_taxonomy.txt
sed -i ':a;N;$!ba;s/ s__\n/\n/g' gg_13_5_taxonomy.txt
sed -i ':a;N;$!ba;s/;\n/\n/g' gg_13_5_taxonomy.txt
sed -i 's/|/; /g' gg_13_5_taxonomy.txt

'''
e=open(sys.argv[1],'r') #input genus list

f=open(sys.argv[2],'r') #gg fastas

h=open(sys.argv[3],'r') #taxonomy key

g=open(sys.argv[4],'w') #outfile - 16s of the genus list

print 'loading seqs'
x = SeqIO.to_dict(SeqIO.parse(f,'fasta'))

tax={}
print 'parsing taxonomy'
for i in h:

	taxid=i.split()[0]
	genus=i.split()[-1]
	genus=genus.rstrip("\n")
	genus=genus.rstrip(";")
	if genus not in tax.keys():
		
		tax[genus]=taxid

print "writing"	

genera=[]
for i in e:
	k=i.rstrip("\n")
	k=k.split("; ")
	genera.append(k)

for i in genera:
	fulltax="; ".join(str(t) for t in i)
	for p in range(1,len(i)):
		
		v=i[-p]
		
		if v in tax.keys():
			
			g.write(">"+fulltax+"\n"+str(x[tax[v]].seq)+"\n")
			
			break
	if v not in tax.keys():
	
		print fulltax,v,"not found"
	
	
	
	
	
	
	
	
	
	
	
	
	
		