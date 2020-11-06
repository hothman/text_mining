# Fetch PMID

The workflow is coded in `fetch_pmid_list.nf` and requires the script `bin/extract_genes.py` to be in the same path. 
The script generates two files, one the PMIDs for each queried contry. You can make modifications to suite your own queries at lines 64 and 67 in `fetch_pmid_list.nf`. The second output is the list of genes extracted from PharmGKB data output to file `pharmgenes_from_phamgkb.txt`.

## Usage
Basic usage will run the default parameters and can be invoked as such: 

```
nextflow run fetch_pmid_list.groovy
```

for more control over the output you can use it in such way:

```
nextflow -log run1.log  run fetch_pmid_list.groovy clean --output pmid_gene_country2.tsv --outputdir ./ 
```
Which will generate a log file `run1.log`, clean up the cache and output the TSV file to `pmid_gene_country2.tsv` in the directory from which you are running the workflow `./`.

## Requirement
  * Entrez Edirect: can be obtained from [](https://www.ncbi.nlm.nih.gov/books/NBK179288/). It can be also installed from [Bioconda channel](https://bioconda.github.io/recipes/entrez-direct/README.html)
  * Python3.
  
 
