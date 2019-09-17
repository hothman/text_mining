
# Description
#### author Houcmeddine Othman, September 2019, [My Github page](https://github.com/hothman) 

The codes in this notebook are written to generate the structure of the database accroding to the ERD including the columns for primary keys and foreign keys. The output are 7 tables in csv format. 

![title](diagram_PM.png)

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

## Completing P-value to SNP and Star tables


```python
import pandas as pd 
import warnings

# read tables 
snp = pd.read_csv("../data/snp_raw.csv")
star = pd.read_csv("../data/star_raw.csv")
curation = pd.read_csv("../data/clean_curation.csv")

# Some variants were discarded in in the curation table, we delete them also from snp and star
ids_in_curation = list( curation.id_in_source )
snp = snp[snp.id_in_source.isin(ids_in_curation)]
star = star[star.id_in_source.isin(ids_in_curation)]

# left joining curation data to snp table
snp = pd.merge(snp, curation[["id_in_source", "P-value"]] , on="id_in_source")

# left joining curation data to star allele table
star = pd.merge(star, curation[["id_in_source", "P-value"]] , on="id_in_source")

# some of the variants are going to be deleted 
var_to_delete = ['1444665865','1444665876', '1444665886', '1449270328', 
 '1449270311', '1449270340', '1184509852','1184509863', '1448105757']

for varID in var_to_delete: 
    snp = snp[snp.id_in_source != int(varID)]   # panas reads var as integer 
    star = star[star.id_in_source != int(varID)]
    curation = curation[curation.id_in_source != int(varID)]

#generating primary keys for snp table 
len_snp = len(snp)
ID_snp = [ "SNP"+str(i) for i in range(1, len_snp+1) ]
snp["ID_snp"] = ID_snp

#generating primary keys for star table 
len_star = len(star)
ID_star = [ "STAR"+str(i) for i in range(1, len_star+1) ]
star["ID_star"] = ID_star

snp
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rs_id</th>
      <th>gene_name</th>
      <th>drug_name</th>
      <th>phenotype</th>
      <th>allele</th>
      <th>reference_id</th>
      <th>source</th>
      <th>id_in_source</th>
      <th>P-value</th>
      <th>ID_snp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>rs28371685</td>
      <td>CYP2C9</td>
      <td>warfarin</td>
      <td>Allele T is associated with decreased dose of ...</td>
      <td>T</td>
      <td>20072124</td>
      <td>PharmGKB</td>
      <td>608431789</td>
      <td>&lt; 0.001</td>
      <td>SNP1</td>
    </tr>
    <tr>
      <td>1</td>
      <td>rs28371686</td>
      <td>CYP2C9</td>
      <td>warfarin</td>
      <td>Allele G is associated with decreased dose of ...</td>
      <td>G</td>
      <td>20072124</td>
      <td>PharmGKB</td>
      <td>608431793</td>
      <td>&lt; 0.001</td>
      <td>SNP2</td>
    </tr>
    <tr>
      <td>2</td>
      <td>rs7900194</td>
      <td>CYP2C9</td>
      <td>warfarin</td>
      <td>Allele A is associated with decreased dose of ...</td>
      <td>A</td>
      <td>20072124</td>
      <td>PharmGKB</td>
      <td>608431781</td>
      <td>0.023</td>
      <td>SNP3</td>
    </tr>
    <tr>
      <td>3</td>
      <td>rs9332131</td>
      <td>CYP2C9</td>
      <td>warfarin</td>
      <td>Genotype DEL is associated with decreased dose...</td>
      <td>DEL</td>
      <td>20072124</td>
      <td>PharmGKB</td>
      <td>608431785</td>
      <td>&lt; 0.001</td>
      <td>SNP4</td>
    </tr>
    <tr>
      <td>4</td>
      <td>rs339097</td>
      <td>CALU</td>
      <td>warfarin</td>
      <td>Allele G is associated with increased dose of ...</td>
      <td>G</td>
      <td>20200517</td>
      <td>PharmGKB</td>
      <td>637879876</td>
      <td>0.03</td>
      <td>SNP5</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>362</td>
      <td>rs1902023</td>
      <td>UGT2B15</td>
      <td>acetaminophen</td>
      <td>Genotype AA is associated with increased metab...</td>
      <td>AA</td>
      <td>28663312</td>
      <td>PharmGKB</td>
      <td>1448639952</td>
      <td>ambiguous</td>
      <td>SNP363</td>
    </tr>
    <tr>
      <td>363</td>
      <td>CYP3A5</td>
      <td>CYP3A5 (PA131)</td>
      <td>acetaminophen</td>
      <td>Allele C is not associated with metabolism of ...</td>
      <td>C</td>
      <td>28663312</td>
      <td>PharmGKB</td>
      <td>1448639975</td>
      <td>&gt; 0.05</td>
      <td>SNP364</td>
    </tr>
    <tr>
      <td>364</td>
      <td>rs8330</td>
      <td>UGT1A</td>
      <td>acetaminophen</td>
      <td>Allele C is not associated with metabolism of ...</td>
      <td>C</td>
      <td>28663312</td>
      <td>PharmGKB</td>
      <td>1448639969</td>
      <td>&gt; 0.05</td>
      <td>SNP365</td>
    </tr>
    <tr>
      <td>365</td>
      <td>rs5333</td>
      <td>EDNRA</td>
      <td>prednisone</td>
      <td>Genotypes CC + CT is associated with increased...</td>
      <td>CC + CT</td>
      <td>30672385</td>
      <td>PharmGKB</td>
      <td>1450367980</td>
      <td>0.016</td>
      <td>SNP366</td>
    </tr>
    <tr>
      <td>366</td>
      <td>rs2273897</td>
      <td>ABCC2</td>
      <td>emtricitabine</td>
      <td>Genotype TT is associated with increased conce...</td>
      <td>TT</td>
      <td>30767719</td>
      <td>PharmGKB</td>
      <td>1450377018</td>
      <td>0.028</td>
      <td>SNP367</td>
    </tr>
  </tbody>
</table>
<p>367 rows × 10 columns</p>
</div>



## generating tables ethnicity_country for snp and star 



```python
regions= list( curation.groupby('region').count().index )
len_regions = len(regions)
ID_region = [ "REGION"+str(i) for i in range(1, len_regions+1) ]
region_table = pd.DataFrame({"id_region":ID_region, "region":regions })

region_table
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_region</th>
      <th>region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>REGION1</td>
      <td>African American/Afro-Caribbean</td>
    </tr>
    <tr>
      <td>1</td>
      <td>REGION2</td>
      <td>Mixed Population containing african descendant...</td>
    </tr>
    <tr>
      <td>2</td>
      <td>REGION3</td>
      <td>North African</td>
    </tr>
    <tr>
      <td>3</td>
      <td>REGION4</td>
      <td>Sub-Saharan African</td>
    </tr>
  </tbody>
</table>
</div>



## generating table for reference


```python
reference = pd.read_csv("../data/referance_raw.csv")
len_reference = len(reference)
ID_reference = [ "REF"+str(i) for i in range(1, len_reference+1) ]
reference["ref_id"]=ID_reference
reference.rename(columns={'external_id': "reference_id"}, inplace=True)
reference.set_index("ref_id", inplace=True)

reference.to_csv("../data/csv4SQL/Study.csv", index=False)


reference.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>reference_id</th>
      <th>type</th>
      <th>year</th>
      <th>title</th>
    </tr>
    <tr>
      <th>ref_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>REF1</td>
      <td>24024897</td>
      <td>PMID</td>
      <td>2013</td>
      <td>RRM1 and RRM2 pharmacogenetics: association wi...</td>
    </tr>
    <tr>
      <td>REF2</td>
      <td>23173844</td>
      <td>PMID</td>
      <td>2012</td>
      <td>PXR and CAR single nucleotide polymorphisms in...</td>
    </tr>
    <tr>
      <td>REF3</td>
      <td>27045425</td>
      <td>PMID</td>
      <td>2016</td>
      <td>CYP2B6 genotype-based efavirenz dose recommend...</td>
    </tr>
    <tr>
      <td>REF4</td>
      <td>15094935</td>
      <td>PMID</td>
      <td>2004</td>
      <td>CYP2C9 genetic polymorphisms and warfarin.</td>
    </tr>
    <tr>
      <td>REF5</td>
      <td>23158458</td>
      <td>PMID</td>
      <td>2013</td>
      <td>Multiple regulatory variants modulate expressi...</td>
    </tr>
  </tbody>
</table>
</div>



## Generating pharmacogenes table 



```python
pharmacogenes = pd.read_csv("../data/genes_prot_chromosome_function.csv")
len_pharmacogenes = len(pharmacogenes)
ID_pharmacogenes = [ "PHARGENE"+str(i) for i in range(1, len_pharmacogenes+1) ]
pharmacogenes["ID_pharmacogenes"] = ID_pharmacogenes 
pharmacogenes.set_index("ID_pharmacogenes", inplace=True)

pharmacogenes.to_csv("../data/csv4SQL/pharmacogenes.csv", index=False)

pharmacogenes.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Chromosome</th>
      <th>gene_name</th>
      <th>Uniprot_ID</th>
      <th>Function</th>
    </tr>
    <tr>
      <th>ID_pharmacogenes</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PHARGENE1</td>
      <td>7</td>
      <td>ABCB1</td>
      <td>P08183</td>
      <td>Translocates drugs and phospholipids across th...</td>
    </tr>
    <tr>
      <td>PHARGENE2</td>
      <td>2</td>
      <td>ABCB11</td>
      <td>O95342</td>
      <td>Catalyzes the secretion of conjugated bile sal...</td>
    </tr>
    <tr>
      <td>PHARGENE3</td>
      <td>10</td>
      <td>ABCC2</td>
      <td>Q92887</td>
      <td>Mediates hepatobiliary excretion of numerous o...</td>
    </tr>
    <tr>
      <td>PHARGENE4</td>
      <td>4</td>
      <td>ABCG2</td>
      <td>Q9UNQ0</td>
      <td>High-capacity urate exporter functioning in bo...</td>
    </tr>
    <tr>
      <td>PHARGENE5</td>
      <td>17</td>
      <td>ACE</td>
      <td>P12821</td>
      <td>Converts angiotensin I to angiotensin II by re...</td>
    </tr>
  </tbody>
</table>
</div>



## Generating drug table


```python
drugs = pd.read_csv("../data/drugs.csv")
len_drugs = len(drugs)
ID_drugs = [ "DRUG"+str(i) for i in range(1, len_drugs+1) ]
drugs["ID_drugs"] = ID_drugs 
drugs.set_index("ID_drugs", inplace=True)
drugs.rename(columns={'Drug name': "drug_name"}, inplace=True)

drugs.to_csv("../data/csv4SQL/drug.csv", index=False)

drugs.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>drug_name</th>
      <th>ID Drug bank</th>
      <th>state</th>
      <th>Indication</th>
      <th>IUPAC_name</th>
    </tr>
    <tr>
      <th>ID_drugs</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>DRUG1</td>
      <td>warfarin</td>
      <td>DB00682</td>
      <td>Approved</td>
      <td>Prophylaxis and treatment of venous thromboemb...</td>
      <td>4-hydroxy-3-(3-oxo-1-phenylbutyl)-2H-chromen-2...</td>
    </tr>
    <tr>
      <td>DRUG2</td>
      <td>haloperidol</td>
      <td>DB00502</td>
      <td>Approved</td>
      <td>Haloperidol is indicated for a number of condi...</td>
      <td>4-[4-(4-chlorophenyl)-4-hydroxypiperidin-1-yl]...</td>
    </tr>
    <tr>
      <td>DRUG3</td>
      <td>clozapine</td>
      <td>DB00363</td>
      <td>Approved</td>
      <td>For use in patients with treatment-resistant s...</td>
      <td>8-Chloro-11-(4-methylpiperazin-1-yl)-5H-dibenz...</td>
    </tr>
    <tr>
      <td>DRUG4</td>
      <td>mephenytoin</td>
      <td>DB00532</td>
      <td>Approved, Investigational, Withdrawn</td>
      <td>For the treatment of refractory partial epilepsy</td>
      <td>5-ethyl-3-methyl-5-phenylimidazolidine-2,4-dione</td>
    </tr>
    <tr>
      <td>DRUG5</td>
      <td>efavirenz</td>
      <td>DB00625</td>
      <td>Approved, Investigational</td>
      <td>(4S)-6-chloro-4-(2-cyclopropylethynyl)-4-(trif...</td>
      <td>(4S)-6-Chloro-4-(cyclopropylethynyl)-1,4-dihyd...</td>
    </tr>
  </tbody>
</table>
</div>



# Arranging secondary keys for SQL implementation

### SNP table


```python
def create_col_from_index(df_on_left, df_On_right, col_to_merge, tag ):
    mydf = df_On_right.copy()
    index_col = mydf.index
    mydf["index_col"] = index_col    
    mydf=mydf.filter(items=['index_col', col_to_merge ] )  
    merged= pd.merge(df_on_left, mydf, on=col_to_merge).drop(columns=[col_to_merge])
    return merged.rename(columns={'index_col': tag} )


# add gene id
snp = create_col_from_index(snp, pharmacogenes , "gene_name", "gene_id" )

# add drug id, corrected later aftergenerating the whole able
snp = create_col_from_index(snp, drugs , "drug_name", "drug_id" )

# add reference id 
snp = create_col_from_index(snp, reference , "reference_id", "reference_id" ) 


# arranging columns 
snp.rename(columns={'ID_snp': "id"}, inplace=True )

snp= snp.filter(items=['id', "rs_id", "drug_id", 
                  "allele", "phenotype", 
                  "reference_id", "P-value", 
                 "source", "id_in_source"])

snp.to_csv("../data/csv4SQL/snp_allele.csv", index=False)

```

### Star allele table


```python
# add gene id
star= create_col_from_index(star, pharmacogenes , "gene_name", "gene_id" )
# add drug id, corrected later aftergenerating the whole able
star = create_col_from_index(star, drugs , "drug_name", "drug_id" )
# add reference id 
star = create_col_from_index(star, reference , "reference_id", "reference_id" ) 
# arranging columns 
star.rename(columns={'ID_star': "id"}, inplace=True )

star= star.filter(items=['id', "star_annotation", "drug_id", 
                  "allele", "phenotype", 
                  "reference_id", "P-value", 
                 "source", "id_in_source"])


star.to_csv("../data/csv4SQL/star_allele.csv", index=False)

```

### snp by country table


```python
merged_countries = pd.merge(snp, curation, on="id_in_source")
merged_countries_snp = merged_countries.filter(items=["id", "region", "Country_of_Participants"]) 
merged_countries_snp.rename(columns={'id': "snp_id"}, inplace=True )
len_merged_countries_snp = len(merged_countries_snp)
ID_countries_snp = [ "SNPREGION"+str(i) for i in range(1, len_merged_countries_snp+1) ]
merged_countries_snp["id"]=ID_countries_snp
merged_countries_snp = merged_countries_snp.filter(items=["id", "snp_id", "region", "Country_of_Participants"])

# output table 
merged_countries_snp.to_csv("../data/csv4SQL/snp_country.csv", index=False)

merged_countries_snp.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>snp_id</th>
      <th>region</th>
      <th>Country_of_Participants</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>SNPREGION1</td>
      <td>SNP1</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>1</td>
      <td>SNPREGION2</td>
      <td>SNP1</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>2</td>
      <td>SNPREGION3</td>
      <td>SNP2</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>3</td>
      <td>SNPREGION4</td>
      <td>SNP2</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>4</td>
      <td>SNPREGION5</td>
      <td>SNP3</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
  </tbody>
</table>
</div>



### star by country 


```python
merged_countries = pd.merge(star, curation, on="id_in_source")
merged_countries_star = merged_countries.filter(items=["id", "region", "Country_of_Participants"]) 
merged_countries_star.rename(columns={'id': "star_id"}, inplace=True )
len_merged_countries_star = len(merged_countries_star)
ID_countries_star = [ "STARREGION"+str(i) for i in range(1, len_merged_countries_star+1) ]
merged_countries_star["id"]=ID_countries_star
merged_countries_star = merged_countries_star.filter(items=["id", "star_id", "region", "Country_of_Participants"])

# output the table
merged_countries_star.to_csv("../data/csv4SQL/star_allele_country.csv", index=False)

merged_countries_star.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>star_id</th>
      <th>region</th>
      <th>Country_of_Participants</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>STARREGION1</td>
      <td>STAR1</td>
      <td>Sub-Saharan African</td>
      <td>Ethiopia</td>
    </tr>
    <tr>
      <td>1</td>
      <td>STARREGION2</td>
      <td>STAR2</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>2</td>
      <td>STARREGION3</td>
      <td>STAR3</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>3</td>
      <td>STARREGION4</td>
      <td>STAR196</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
    <tr>
      <td>4</td>
      <td>STARREGION5</td>
      <td>STAR197</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python

```
