#!/usr/bin/env python3

#change above if your python 3 environment has a different name

#usage:
#species2taxid.py list-of-species.txt outputfile.txt


import sys
from Bio import Entrez

def get_taxid(species):
	"""to get data from ncbi taxomomy, we need to have the taxid.  we can
	get that by passing the species name to esearch, which will return
	the tax id"""
	
	if len(species.split(" "))==2:
		species = species.replace(" ", "+").strip()
		
		try:
			search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
	
			record = Entrez.read(search)
		
			return record['IdList'][0]
			
		except:
		
			try:
				species = species.split("+")[0] #try just the genus
				search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
				record = Entrez.read(search)
				return record['IdList'][0]
				
			except:
				return "failed"
			
	if len(species.split(" "))==1:
		
		try:
			search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
	
			record = Entrez.read(search)
		
			return record['IdList'][0]
			
		except:
			return "failed"
		

def get_tax_data(taxid):
	"""once we have the taxid, we can fetch the record"""
	search = Entrez.efetch(id = taxid, db = "taxonomy", retmode = "xml")
	return Entrez.read(search)


def main():


	Entrez.email = "theodore.allnutt@rbg.vic.gov.au"
	
	f = open(sys.argv[1],'r')
	g = open(sys.argv[2],'w')
	
	for i in f:
		species_name = i.rstrip("\n")
	
		taxid = get_taxid(species_name)
		
		if taxid!="failed":
			data = get_tax_data(taxid)
			lineage=""
			#lineage = data[0]['LineageEx']['ScientificName']
			try:
				for j in data[0]['LineageEx']:
					if j['Rank']=='superkingdom':
						lineage=lineage+j['ScientificName']
					if j['Rank']=='kingdom':
						lineage=lineage+";"+j['ScientificName']
					if j['Rank']=='phylum':
						lineage=lineage+";"+j['ScientificName']
					if j['Rank']=='class':
						lineage=lineage+";"+j['ScientificName']
					if j['Rank']=='order':
						lineage=lineage+";"+j['ScientificName']
					if j['Rank']=='family':
						lineage=lineage+";"+j['ScientificName']
					if j['Rank']=='genus':
						lineage=lineage+";"+j['ScientificName']
				lineage=lineage+";"+species_name
				
				g.write(species_name+"\t"+taxid+"\t"+lineage+"\n")
				print(species_name,taxid,lineage)
			except:
				print(species_name,taxid,lineage,"fault")
		else:
		
			g.write(species_name+"\tno_taxid_found\n")
			print(species_name,"failed")
		

if __name__ == '__main__': main()
