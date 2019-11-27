#!/usr/bin/python3
__author__ = "Houcemeddine Othman"
__credits__ = "Wits University, Sydney Brenner Institute for Molecular Bioscience"
__maintainer__ = "Houcemeddine Othman"
__email__ = "houcemoo@gmail.com"

import pubmed_parser as pp                # I need this only to get an easy access 
import xml.etree.ElementTree as ET        #to multiple Pubned xmls, this is just a lasy way to do it
import sys 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer
import argparse

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

def get_data(xmlfile): 
	get_dic = pp.parse_medline_xml(xmlfile)[0]
	return get_dic

def joinAbsTit(medlineDic): 
	abstract = medlineDic['abstract']
	title = medlineDic['title']
	return str(abstract)+" "+str(title)

def tokenize_remove_stop_words_stemmize(text): 
	tokenized_text=word_tokenize(text.lower())
	
	filtered_words = [word for word in tokenized_text if word not in stopwords.words('english')]
	stemmer = SnowballStemmer("english")
	stemmed_words = [ stemmer.stem( word  ) for word in filtered_words ]
	return stemmed_words

def get_lexicon(lexicon):
	with open(lexicon, 'r') as file:
		lexicon = file.read().lower().splitlines() 
	lexicon = [word for word in lexicon if word not in ["ga", "san"]]
	return lexicon

def check_occurence(lexicon, corpus):
	for word in corpus: 
		if word in lexicon and (word !="ga" or word !="san") :
			return "PASS", word
	return "FAIL", "NO_HIT"


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Mining Medline Absracts for a list of queries")
	parser.add_argument("--query", help="file containing the list of words to search for")
	parser.add_argument("--xml", help="Path to medline XML format ")
	parser.add_argument("--output", help="outputfile ")
	args = parser.parse_args()
	medline_dictionary = get_data(args.xml)
	text_to_mine = joinAbsTit(medline_dictionary)
	PMID = medline_dictionary["pmid"]
	query_terms = get_lexicon( args.query )
	tokenized = tokenize_remove_stop_words_stemmize( text_to_mine )
	is_pass, word = check_occurence(query_terms, tokenized)
	print(PMID,"\t",is_pass, "\t", word)
	with open( args.output , 'w') as file:
		file.writelines( '\t'.join( [PMID,is_pass, word]  )+'\n' )
