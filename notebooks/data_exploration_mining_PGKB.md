
# Description
#### author Houcmeddine Othman, September 2019, [My Github page](https://github.com/hothman) 

The codes in this notebook are written for:

* reading the data in PGKB. 
* Generating bibliography references list to be used for manual curation later. 
* Data wrangling for multiple genes and multiple drug entries
* Parsing XML medline data.
* In general providing clean raw data before generating the tables according to the Entity-relationship model for the database. 

### requirements:
* Python 3
* Pandas, numpy, pubmed_parser

---
## Credits
### Without the contribution of these people, I would end up with ugly empty output files and big ERROR message. 

#### Manual Curation (in alphabetical order) 
Ayoub Ksouri, Chaimae SAMTAL, Chiamaka Jessica Okeke, Fouzia Radouani, Haifa Jmal, Kais Ghedira, Lyndon Zass, Melek Chaouch, Olivier, Reem Sallam, Rym Kefi, Samah Ahmed, Samar kamel Kassem, Yosr Hamdi.

#### Data mining and wrangling
Jorge da Rocha and Lyndon Zass


## Data exploration of PGKB data 


```python
import pandas as pd 

pheno=pd.read_csv("../data/annotation/var_pheno_ann.tsv", delimiter="\t")
drug=pd.read_csv("../data/annotation/var_drug_ann.csv", delimiter="\t")

pmid = pd.read_csv("../data/pubmed_ids_list_PGKB_09Aug2019.csv", header=None, names=["PMID"])

def getPMID(dataframe): 
    return dataframe["PMID"].unique() 

uniquePMID = getPMID(pmid)
len(uniquePMID)

```




    6375



# Cleaning data for curation (PhamGKB)

I will join the PMID from the text mining study 


```python
#read the pmid identified by text mining 
drug=pd.read_csv("../data/annotation/var_drug_ann.csv", delimiter="\t")
pmid_africans=pd.read_csv("../data/is_african_pharmgkb_PASS.tsv", delimiter="\t", header=None, 
                          names=["PMID", "filter", "hit"])
# read Jorge's file
Jorge_filtering=pd.read_csv("../data/Jorge_filtering/African_NorthAf_and_AF_Amer_PharmGKB_vardrug.txt", delimiter="\t")
print("number of variants in Jorge's file\t", len(Jorge_filtering))

joined_drug=pd.merge(pmid_africans["PMID"], drug, on='PMID', how='inner')
print("number of variants in text mining identified variants\t", len(joined_drug))

# merge Jorge's data and my data
result = Jorge_filtering.append(joined_drug, sort=False)

# remove duplicates based on annotation ID
result=result.drop_duplicates(subset='Annotation ID', keep='first')
print("number of total variants\t", len(result))

result.to_csv('../data/filtered_entries_phamGKB.csv', index=False)

```

    number of variants in Jorge's file	 441
    number of variants in text mining identified variants	 222
    number of total variants	 479


## extract data from PharmGKB


```python
import pandas as pd

pgkb_data = pd.read_csv("../data/filtered_entries_phamGKB.csv")

pgkb_data.dtypes

```




    Annotation ID           int64
    Variant                object
    Gene                   object
    Chemical               object
    PMID                    int64
    Phenotype Category     object
    Significance           object
    Notes                  object
    Sentence               object
    StudyParameters        object
    Alleles                object
    Chromosome             object
    Unnamed: 12           float64
    Unnamed: 13           float64
    Unnamed: 14           float64
    Unnamed: 15           float64
    dtype: object



Many of the entries contain multiple genes per. I a; splitting them to generate the full list


```python
# some of the entries contain many genes 
# so we need to split them
gene_names = []
for gene in pgkb_data["Gene"]: 
    for element in ( str(gene).split()): 
        if "(" not in element: 
            gene_names.append(element)

genes = pd.DataFrame({"gene_name":gene_names })
genes.drop_duplicates(inplace=True)
# remove contaminaiting nan as object
genes=genes[genes.gene_name != 'nan']
genes.to_csv("../data/gene_name_list.csv", index=False)

```


```python
def clean_star_allele(dataframe): 
    mydataframe =  dataframe[["Variant", "Chemical", "PMID", "Chromosome", "Annotation ID", "Gene"]]
    print(mydataframe["Chemical"].split(",")) 

dataframe_star = pd.DataFrame()
star_notation, pgkb_id, gene_name, drug_name, PMID, phenotype, allele =  ([] for i in range(7))

for index, variant in enumerate(pgkb_data["Variant"]): 
    if "*" in variant :
        splitted_star_alleles = variant.split(",")
        for star_allele in splitted_star_alleles:  
            raw= list(pgkb_data.loc[index])
            raw[1]=star_allele
            star_notation.append(star_allele.strip())
            #print(raw)
            #print(raw[9:11])
            pgkb_id.append( raw[0] )
            gene_name.append( raw[2].split()[0].strip() )
            drug_name.append( raw[3].split()[0].strip() )
            PMID.append( raw[4] )
            phenotype.append( raw[8] )
            allele.append( raw[10] )

source=["PharmGKB"]*len(star_notation)

star_alleles = { "star_annotation": star_notation, 
        "drug_name": drug_name,"gene_name":gene_name, 
        "phenotype":phenotype, "allele":allele,  "reference_id":PMID, 
       "source":source, "id_in_source":pgkb_id }

dataframe_star = pd.DataFrame(star_alleles)

dataframe_star.to_csv("../data/star_raw.csv", index=False)
```

## Cleansing of SNP data


```python
# these variants have more than one gene and are corrected based on dbsnp 
# manually 


to_correct = {"rs9934438":"VKORC1", "rs776746":"CYP3A5", "rs17886199":"VKORC1", 
             "rs12979860":"IFNL4", "rs41303343":"CYP3A5", "rs10264272":"CYP3A5", 
             "rs776746":"CYP3A5", "rs429358":"APOE", "rs7412":"APOE", "rs12979860":"IFNL4", 
              "rs34650714":"UGT1A1"}

dataframe_snp = pd.DataFrame()
rs_id, pgkb_id, gene_name, drug_name, PMID, phenotype, allele =  ([] for i in range(7))

for index, variant in enumerate(pgkb_data["Variant"]): 
    if "*" not in variant and ("rs" in variant): 
        raw = list(pgkb_data.loc[index])
        
        # correct gene names from to_correct dictionary 
        if raw[1] in to_correct.keys() : 
            raw[1] = to_correct[raw[1]]  
        
        # gene name but remove the second part
        else:
            raw[2]=str(raw[2]).split()[0]
            
        drugs = raw[3].split(",") 
        for drug in drugs :   
            raw[3] =  drug.split()[0]
        rs_id.append(  raw[1] )
        pgkb_id.append(  raw[0] )
        gene_name.append(raw[2])
        drug_name.append( raw[3] )
        PMID.append( raw[4] )
        phenotype.append( raw[8] )
        allele.append( raw[10] ) 
        
source=["PharmGKB"]*len(pgkb_id)
       
snps = { "rs_id": rs_id,  "gene_name":gene_name, 
        "drug_name": drug_name, "phenotype":phenotype, "allele":allele,  "reference_id":PMID, 
        "source":source, "id_in_source":pgkb_id }
        
dataframe_snp = pd.DataFrame(snps)

dataframe_snp.replace(to_replace="uric", value='uric acid', regex=True, inplace=True)

dataframe_snp.to_csv("../data/snp_raw.csv", index=False)
```


```python
# this list will serve me to download the medline data in xml format
pgkb_data["PMID"].drop_duplicates().to_csv("../data/PMIDs_pgkb_data.csv", index=False)
```

    /home/houcemeddine/modules/anaconda/3.7/lib/python3.7/site-packages/ipykernel_launcher.py:2: FutureWarning: The signature of `Series.to_csv` was aligned to that of `DataFrame.to_csv`, and argument 'header' will change its default value from False to True: please pass an explicit value to suppress this warning.
      


## preparing references table
PMIDs are extracted to a one column csv file which was then processed by the script `construct_ref_xml.sh`. Using edirect, entries where downloaded with their xml files. 



```python
import pubmed_parser as pp   # I need this only to get an easy access 
                            #to multiple Pubned xmls, this is just a lasy way to do it
import xml.etree.ElementTree as ET 

path_xml = pp.list_xml_path('../data/xml_references/') # list all xml paths under directory

# the function parses xml files and extract PMID, publication year and paper title
def ParsePMEDXML(xmlfile):
    tree = ET.parse(xmlfile) 
    root = tree.getroot()
    PMID = tree.findall('PubmedArticle/MedlineCitation/PMID') 
    pmid = PMID[0].text
    YEAR = tree.findall('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year') 
    try:
        year = YEAR[0].text
    except: 
        # new articles don t have Year element under Pbdate
        YEAR = tree.findall('PubmedArticle/MedlineCitation/DateRevised/Year') 
        year=YEAR[0].text
    Title = tree.findall('PubmedArticle/MedlineCitation/Article/ArticleTitle') 
    title = Title[0].text
    return pmid, year, title

# iteratte over the list of xml files
id=[]; ti = []; yy = []
for reference_file in path_xml : 
    pmid, year, title = ParsePMEDXML(reference_file)
    id.append(pmid)
    yy.append(year)
    ti.append(title)
    
type = len(ti)*['PMID']

reference_raw = pd.DataFrame({"external_id":id, "type":type, "year":yy, "title":ti})

reference_raw.to_csv("../data/referance_raw.csv", index=False)
```
