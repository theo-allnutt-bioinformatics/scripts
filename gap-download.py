#!/usr/bin/env python3

import ckanapi
import datetime
import os
import requests
import sys
import subprocess as sp
import concurrent.futures
#import pprint

#Downloads files form GAP data portal

#gap-download.py samples.txt outfolder/ 8

#Where samples.txt is a text file of your search terms, one term for each row. If a term hits more than one file url, all files will be downloaded. '8' is the number of threads to use for downloading file sin parallel.

#https://usersupport.bioplatforms.com/find_filter_download.html

#Do not use booleans with fields, only in simple text e.g. one field only: "sample_id:102.100.100/79784" or a text string: "79784 AND 81963", which gets sample 79784 library 81963 only.


#https://toolkit.data.wa.gov.au/hc/en-gb/articles/4413492209935-Search-using-Solr-query-language


#Search fields that can be specified:'access_control_date', 'access_control_mode', 'access_control_reason', 'analysissoftwareversion', 'author', 'author_email', 'bait_set_name', 'bait_set_reference', 'base_url', 'ccg_jira_ticket', 'creator_user_id', 'data_generated', 'data_type', 'dataset_id', 'date_data_published', 'date_of_transfer', 'date_of_transfer_to_archive', 'description', 'dna_extract', 'dna_extract_pressed_sheet', 'download', 'facility', 'family', 'flow_cell_id', 'folder_name', 'genomic_material_associated_references', 'genomic_material_preparation_date', 'genomic_material_preparation_materials', 'genomic_material_preparation_process', 'genomic_material_preparation_type', 'genomic_material_prepared_by', 'herbarium_code', 'id', 'id_vetting_by', 'isopen', 'library_construction_protocol', 'library_id', 'license_id', 'license_title', 'living_collections_catalog_number', 'living_collections_material_sample_rna', 'living_collections_record_number', 'living_collections_recorded_by', 'maintainer', 'maintainer_email', 'metadata_created', 'metadata_modified', 'nagoya_protocol_compliance', 'nagoya_protocol_permit_number', 'name', 'notes', 'num_resources', 'num_tags', 'organization', 'owner_org', 'preservation_temperature', 'preservation_type', 'private', 'project_aim', 'resource_permissions', 'sample_id', 'sample_submitter_email', 'sample_submitter_name', 'scientific_name', 'scientific_name_authorship', 'scientific_name_notes', 'sequence_data_type', 'sequencer', 'silica_gel', 'silica_gel_id', 'silica_gel_pressed_sheet', 'state', 'ticket', 'title', 'type', 'url', 'version', 'voucher_herbarium_catalog_number', 'voucher_herbarium_collector_id', 'voucher_herbarium_record_number', 'voucher_herbarium_recorded_by', 'resources', 'tags', 'groups', 'relationships_as_subject', 'relationships_as_object'


remote = ckanapi.RemoteCKAN('https://data.bioplatforms.com', apikey='705a5c04-68d4-49a0-bf90-b637e81d6bbb')
#If this key has expired, you will need to obtain a new one from bioplatforms.


def gap_search(value1):
	
	data = remote.action.package_search(q=f"{value1}",rows=50000,include_private=True)
	print(value1,len(data))
	#print(data)
	return data

def download(i):
	value1=i.rstrip("\n")
	result=(gap_search(value1))
	
	print(type(result['results']),len(result['results']))

	for package in result['results']:

		#print(package)
		
		if 'scientific_name' in package.keys():
			g2.write(value1+"\t"+package['scientific_name']+"\n")	
		else:
			g2.write(value1+"\t"+"species name not found\n")
		
		for resource in package['resources']:
				
			url = resource['url']
			
			#resp = requests.get(resource['url'], headers={'Authorization': remote.apikey})
				
			filename=url.split("/")[-1]
			
			print("downloading",url)
			
			#input()
			
			p0=sp.Popen('curl -O -L -C - -H "Authorization: 705a5c04-68d4-49a0-bf90-b637e81d6bbb" "{}"'.format(url),shell=True).wait()
			p1=sp.Popen("mv {} {}".format(filename,outfolder+"/"),shell=True).wait()
			
			
#######global

f=open(sys.argv[1],'r')
	
outfolder=sys.argv[2]



threads=int(sys.argv[3])

g2=open("sample_list_spp.txt",'a')

if __name__ == '__main__':
		
	executor1 = concurrent.futures.ProcessPoolExecutor(threads)
	futures1 = [executor1.submit(download,i) for i in f]
	concurrent.futures.wait(futures1)

	#for i in f:
	
		#download(i)
	
					
					
					
	