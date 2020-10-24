#!usr/bin/env nextflow 
/*
 	Author: Houcemeddine Othman
 	 	https://github.com/hothman
 	 	houcemoo@gmail.com
 	Sydney Brenner Institute for Molecular Bioscience - Wits University, 2019
 	--------------------------------------------------------------------------------------
 	Workflow for mining Medline entries
	Requires edirect tools to be in PATH
 	params: PYTHONPATH path to python executable 
 			SCRIPTPATH path to the script text_mining.py 
 			myList List of terms to search for 
 			MAXFORKS number of cores to use 
 	---------------------------------------------------------------------------------------
 	PMID_list: Provide a list of pubmed IDs in a plain ext format (one accession per line) 
 	The results are collected in "output_path" 
*/ 


//This step aims to retreive all the bibliography ressources about any of the pharmacogenes described
//from PharmGKB in North African region (Morocco, Algeria, Tunisia, Libya, Egypt, Sudan and Mauritania)

//fetch the list of variants from PharmGKB

params.PKGDATA  = '/home/houcemeddine/BILIM/PGx-North_africa/fetch_pmid_list/annotations.zip'
process extract_gene_list {
	
	output: 
		file "pharmgenes_from_phamgkb.txt" into gene_list

	"""
	# wget https://api.pharmgkb.org/v1/download/file/data/annotations.zip
	unzip ${params.PKGDATA}
	extract_genes.py
	sort temp_list_genes |uniq |head -n 10 > pharmgenes_from_phamgkb.txt 
	"""
}


gene_list.flatMap()
     .subscribe { println "File: ${it.name} => ${it.text}" }


process get_medline {
	//errorStrategy 'ignore'
	cpus 1

	input: 
		val gene from gene_list.splitText().flatMap()

	output: 
		file "output_all_genes.tsv" into pmid_file

	

	"""
	for query in  Tunisia  Egypt
	do
	echo $gene 
	sleep 5
	echo "esearch -db pubmed -query '\${query}[AD]  AND CYP2D6' | efetch -format uid > pmids_\${query}.txt" >command.sh
	sh command.sh
	nb=\$(wc -l pmids_\${query}.txt |awk {'print \$1'})  # get number of lines
	DIFFERENCE=\$((nb-1))
	printf "${gene}\n%.0s" `seq \$DIFFERENCE` \$DIFFERENCE |sed  '/^\$/d' >\${query}_genes.txt
	printf "\$query\n%.0s" `seq \$DIFFERENCE` \$DIFFERENCE |sed  '/^\$/d' >\${query}_country.txt
	paste pmids_\${query}.txt \${query}_genes.txt \${query}_country.txt | column -s \$'\t' -t  >> output_all_genes.tsv

	done
	"""
}


data_vars = pmid_file.collectFile()

process clean {

	input: 
		file list from data_vars

	output: 
		file "pmid_gene_country.tsv"

	publishDir '/home/houcemeddine/BILIM/PGx-North_africa/fetch_pmid_list' , mode:'copy'

	"""
	cat $list >>pmid_gene_country.tsv
	"""

}

