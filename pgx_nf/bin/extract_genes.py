#!/usr/bin/python3
__author__ = "Houcemeddine Othman"
__credits__ = "Wits University H3Africa/GSK ADME project"
__maintainer__ = "Houcemeddine Othman"
__email__ = "houcemoo@gmail.com"

def extractGenes(inputfile,outpufile ):
    with open(inputfile, 'r') as file: 
        lines = file.readlines()
        for line in lines[1:]: 
            gene_line = line.split("\t")[2]
            if gene_line == '':
               pass
            else:
                list_entries = gene_line.split(';')
                list_entries = [element.split() for element in list_entries]
                for gene in list_entries:
                    with open(outpufile,'a') as theoutput: 
                        theoutput.write(gene[0].replace("\"", "")+'\n')

extractGenes("clinical_ann_metadata.tsv", "temp_list_genes" )
extractGenes("var_drug_ann.tsv", "temp_list_genes" )
extractGenes("var_fa_ann.tsv", "temp_list_genes" )
