#!usr/bin/env nextflow 
/*
 	Author: Houcemeddine Othman
 	 	https://github.com/hothman
 	 	houcemoo@gmail.com
 	Sydney Brenner Institute for Molecular Bioscience - Wits University, 2019
 	--------------------------------------------------------------------------------------
 	Workflow for mining Medline entries
 	to retreive all the bibliography ressources about any of the pharmacogenes described
    from PharmGKB in North African region (Morocco, Algeria, Tunisia, Libya, Egypt, Sudan and Mauritania)
	Requires edirect tools to be in PATH
 	params: OUTPUTDIR directory for the output 
 	
 	The a bin directory containing the extract_genes.py script must be in the same path of this script 

 	OUTPUT: returns a TSV file specified by the parameter OUTPUTFILE and the list of unique gene names from 
 		Phamgkb pmid_gene_country.tsv 

 	USAGE: 
 		Basic run: 
 			nextflow run fetch_pmid_list.groovy 

 		More controle on the output:
 			nextflow -log run1.log  run fetch_pmid_list.groovy clean --output pmid_gene_country2.tsv --outputdir ./ 

*/ 

//fetch the list of variants from PharmGKB
params.outputdir = './'
params.output = "pmid_gene_country.tsv"
process extract_gene_list {
	
	output: 
		file "pharmgenes_from_phamgkb.txt" into gene_list

	publishDir params.outputdir , mode:'copy'

	"""
	wget https://api.pharmgkb.org/v1/download/file/data/annotations.zip
	unzip annotations.zip
	extract_genes.py
	sort temp_list_genes |uniq > pharmgenes_from_phamgkb.txt 
	"""
}

gene_list.flatMap()
     .subscribe { println "File: ${it.name} => ${it.text}" }


// Query the different contries in english and frensh 
process get_medline {
	errorStrategy 'retry'
	maxRetries 10
	cpus 1
	echo true

	input: 
		val gene from gene_list.splitText().flatMap()

	output: 
		file "output_all_genes.tsv" into pmid_file
		
	"""
	for query in  Tunisia  Tunisie Maroc  Morocco  Algérie  Algeria  Mauritanie  Mauritania  libya  Egypt  Sudan   
	do
	sleep 5
	echo "esearch -db pubmed -query '\${query}[AD]  AND ${gene}[GENE]' | efetch -format uid > pmids_\${query}.txt" >command.sh
	
	sh command.sh
	echo "EXIT STATUS for searching ENTREZ  \$?"
	nb=\$(wc -l pmids_\${query}.txt |awk {'print \$1'})  # get number of lines
	DIFFERENCE=\$((nb-1))
	echo "Search papers for GENE: ${gene}   QUERY:\$query     NUMBER OF PAPERS:\$nb  \n"
	printf "${gene}\n%.0s" `seq \$DIFFERENCE` \$DIFFERENCE |sed  '/^\$/d' >\${query}_genes.txt
	printf "\$query\n%.0s" `seq \$DIFFERENCE` \$DIFFERENCE |sed  '/^\$/d' >\${query}_country.txt
	paste pmids_\${query}.txt \${query}_genes.txt \${query}_country.txt | column -s \$'\t' -t  >> output_all_genes.tsv

	done
	"""
}


data_vars = pmid_file.collectFile()
// Clean and generate output data
process clean {

	input: 
		file list from data_vars

	output: 
		file params.output

	publishDir params.outputdir , mode:'copy'

	"""
	cat $list |awk  'NF == 3' >> temp
	sed -i 's/Tunisie/Tunisia/'  temp
	sed -i 's/Maroc/Morocco/'  temp
	sed -i 's/Algérie/Algeria/'  temp
	sed -i 's/Mauritanie/Mauritania/'  temp
	sort   temp |uniq > ${params.output}
	"""
}

