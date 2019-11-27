#!usr/bin/env nextflow 
/*
 	Author: Houcemeddine Othman
 	 	https://github.com/hothman
 	 	houcemoo@gmail.com

 	Sydney Brenner Institute for Molecular Bioscience - Wits University, 2019
 	--------------------------------------------------------------------------------------
 	Workflow for mining Medline entries for the developing of Precision Medicine Portal, H3ABionet
	Requires edirect tools to be in PATH
 	params: PYTHONPATH path to python executable 
 			SCRIPTPATH path to the script text_mining.py 
 			myList List of terms to search for 
 			MAXFORKS number of cores to use 
 	---------------------------------------------------------------------------------------
 	PMID_list: Provide a list of pubmed IDs in a plain ext format (one accession per line) 
 	The results are collected in "output_path" 
*/ 

params.myList = "/home/houcemeddine/BILIM/precesion_med/workflow/query_terms.txt" 
params.PYTHONPATH = "/home/houcemeddine/modules/anaconda/3.7/bin/python"
params.SCRIPTPATH = "/home/houcemeddine/BILIM/precesion_med/workflow/bin/"
params.MAXFORKS = 4
PMID_list = file('/home/houcemeddine/BILIM/precesion_med/workflow/pmid.txt')
output_path="/home/houcemeddine/BILIM/precesion_med/workflow/mining_PubMed.txt"

lines = PMID_list.readLines()

process dowmloadXML {
	errorStrategy 'ignore'   // necessary if the client could not connect to NCBI server
	maxForks params.MAXFORKS

	input:
		val line from lines
	output: 
		file "${line}.out" into passOrNot 

	"""
	# requires edirect package
	esearch -db pubmed -query '$line[uid]' |efetch -format xml  >${line}.xml 
	sleep 5
	'${params.PYTHONPATH}' '${params.SCRIPTPATH}'/text_mining.py --xml ${line}.xml --query '${params.myList}' --output ${line}.out 
	rm ${line}.xml
	"""
}

// outputs values to a file
passOrNot.collectFile( name: output_path , newLine: false )
