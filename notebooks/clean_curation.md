
# Description
#### author Houcmeddine Othman, September 2019, [My Github page](https://github.com/hothman) 

The codes in this notebook are part of data cleaning workflow for the manually curated data (raw file is xlsx format).
Some of the tasks include: 
* Discard some contaminating data. 
* Normalizing some labels for the classes description. 

### requirements:
* Python 3
* Pandas, numpy

---
## Credits
### Without the contribution of these people, I would end up with ugly empty output files and big ERROR message. 

#### Manual Curation (in alphabetical order) 
Ayoub Ksouri, Chaimae SAMTAL, Chiamaka Jessica Okeke, Fouzia Radouani, Haifa Jmal, Kais Ghedira, Lyndon Zass, Melek Chaouch, Olivier, Reem Sallam, Rym Kefi, Samah Ahmed, Samar kamel Kassem, Yosr Hamdi.

#### Data mining and wrangling
Jorge da Rocha and Lyndon Zass

## Cleansing of the curation document


```python
import pandas as pd 
import numpy as np

# reading excel file requires xlrd ( conda install -c anaconda xlrd )
data = pd.read_excel("../data/curation_22Aug.xlsx")

# replace URL links and renaming columns 
data.replace(to_replace="https://www.pharmgkb.org/variantAnnotation/", value='', regex=True, inplace=True)
data.replace(to_replace="https://www.ncbi.nlm.nih.gov/pubmed/", value='', regex=True, inplace=True)
data.rename(columns={'link_to_variant': 'id_in_source', 'pubmed_link ': 'reference_id' ,
                     'Country of Participants':'Country_of_Participants'}, inplace=True)
```

Let is check the categories in PharmGKB Category.


```python
data.groupby(["PharmGKB Category"]).count()
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
      <th>id_in_source</th>
      <th>reference_id</th>
      <th>P-value</th>
      <th>Country_of_Participants</th>
      <th>Volunteer 1</th>
      <th>Volunteer 2</th>
      <th>IF No p value - not BLANK use @</th>
      <th>Remarks</th>
    </tr>
    <tr>
      <th>PharmGKB Category</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>African American/Afro-Caribbean</td>
      <td>224</td>
      <td>224</td>
      <td>224</td>
      <td>223</td>
      <td>224</td>
      <td>224</td>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <td>East Asian</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>European</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>4</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Mixed Population</td>
      <td>24</td>
      <td>24</td>
      <td>24</td>
      <td>23</td>
      <td>24</td>
      <td>12</td>
      <td>15</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Near Eastern</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Sub-Saharan Africa</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Sub-Saharan African</td>
      <td>166</td>
      <td>166</td>
      <td>166</td>
      <td>166</td>
      <td>166</td>
      <td>166</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



Some changings to be done: 
* Study from reference PMID25393304 used egyptian subjects as control group. 
* Study from PMID29580174 contains only finnish subjects
* remove East Asian
* use only one notation for Sub-Saharan African
    
Let's now check the categories in country of participents 


```python
data
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
      <th>id_in_source</th>
      <th>reference_id</th>
      <th>P-value</th>
      <th>PharmGKB Category</th>
      <th>Country_of_Participants</th>
      <th>Volunteer 1</th>
      <th>Volunteer 2</th>
      <th>IF No p value - not BLANK use @</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>608431789</td>
      <td>20072124</td>
      <td>&lt; 0.001</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
      <td>Jorge</td>
      <td>Chaimae</td>
      <td>IF multiple p values - ERROR</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>1</td>
      <td>608431793</td>
      <td>20072124</td>
      <td>&lt; 0.001</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
      <td>Samar/done</td>
      <td>Kais</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>2</td>
      <td>608431781</td>
      <td>20072124</td>
      <td>0.023</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
      <td>Samar/done</td>
      <td>Kais</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>3</td>
      <td>608431785</td>
      <td>20072124</td>
      <td>&lt; 0.001</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
      <td>Samar/done</td>
      <td>Kais</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>4</td>
      <td>637879876</td>
      <td>20200517</td>
      <td>0.03</td>
      <td>African American/Afro-Caribbean</td>
      <td>USA</td>
      <td>Samar/done</td>
      <td>Kais</td>
      <td>NaN</td>
      <td>NaN</td>
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
    </tr>
    <tr>
      <td>474</td>
      <td>1449270311</td>
      <td>29580174</td>
      <td>ERROR</td>
      <td>European</td>
      <td>Finland</td>
      <td>Kais</td>
      <td>Olivier</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>475</td>
      <td>1449270340</td>
      <td>29580174</td>
      <td>0.016</td>
      <td>European</td>
      <td>Finland</td>
      <td>Kais</td>
      <td>Olivier</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>476</td>
      <td>1450367980</td>
      <td>30672385</td>
      <td>0.016</td>
      <td>Sub-Saharan African</td>
      <td>Egypt</td>
      <td>Kais</td>
      <td>Olivier</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>477</td>
      <td>1450377018</td>
      <td>30767719</td>
      <td>0.028</td>
      <td>Sub-Saharan African</td>
      <td>NIgeria</td>
      <td>Kais</td>
      <td>Olivier</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>478</td>
      <td>1447990796</td>
      <td>8971426</td>
      <td>@</td>
      <td>Sub-Saharan African</td>
      <td>Zimbabwe</td>
      <td>Kais</td>
      <td>Olivier</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>479 rows × 9 columns</p>
</div>




```python
data.replace("Sub-Saharan Africa", "Sub-Saharan African", inplace=True)


# remove a studyfrom PMID25393304
var_to_remove = []
for varid in list(data[data["reference_id"] == "25393304"].id_in_source) : 
    var_to_remove.append(varid)

# study from finland will be removed
for varid in list(data[data["reference_id"] == "29580174"].id_in_source) : 
    var_to_remove.append(varid)

# Remove Finland, Germany & Egypt (study PMID25393304) Oman, Israel, East Asian
index_to_remove = data[data['Country_of_Participants'].isin(['Germany & Egypt', 'Oman', 'Israel', 'Finland'])].index
data.drop(index_to_remove, inplace = True)

# remove East Asians from the table 
index_to_remove = data[data['PharmGKB Category'] == 'East Asian'].index
data.drop(index_to_remove, inplace = True)

# Change the tag for mixed population
data["PharmGKB Category"].replace({"Mixed Population":"Mixed Population containing african descendant groups"}, inplace = True)

index_to_remove = data[data["PharmGKB Category"] == "European"].index
data.drop(index_to_remove, inplace = True)

```

### correct entries from near eastern countries: 
* Assign "north africa" to Tunisia, Egypt, Morocco


```python
cp = data[data["PharmGKB Category"].str.contains("Near Eastern", na=False)] 
data["PharmGKB Category"].replace({"Near Eastern":"North African"}, inplace = True)
```

### Replacing "@" and "ERROR"


```python
data["P-value"].replace({"@":"", "ERROR":"ambiguous"}, inplace = True)
```

### Rename columns and output to csv



```python
data.rename(columns={'PharmGKB Category': 'region'}, inplace=True)
data.drop(columns=["Remarks"], inplace=True)

data.to_csv("../data/clean_curation.csv", index=False)
```


```python

```
