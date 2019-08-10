#!/usr/bin/python3
__author__ = 'Houcemeddine Othman'
__date__ = '2019' 

import sys 
import re 
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer
from nltk import WordNetLemmatizer

inputfile = "./onepaper.txt"
myMEDLINE  = open(inputfile, 'r' )
Medlinetxt = myMEDLINE.read()
myMEDLINE.close()

def parse(text):
	hh = text.split(r'PMID-')
	mytext=[]
	for elem in hh:
		mysplit = elem.split(r'AB  -')
		mysplit2 = mysplit[-1].split(r'FAU -') 
		#print("###########################") 
		text = mysplit2[0].replace('\n      ', '\n')
		mytext.append( text.replace('\n', ' ')  ) 
	return ' '.join( mytext )

	
def get_title(text):
	mytext=text.split("\n")
	for line in mytext:
		if "TI  - " in line:
			title = line.split("TI  - ")[1]
			return title 

def tokenize_remove_stop_words(text): 
	tokenized_text=word_tokenize(text.lower())
	filtered_words = [word for word in tokenized_text if word not in stopwords.words('english')]
	stemmer = SnowballStemmer("english")
	stemmed_words = [ stemmer.stem( word  ) for word in filtered_words ]
	return stemmed_words

def get_coutries_nationalities(country_list_file, file_nationalities):
	with open(country_list_file, 'r') as file:
		countries = file.read().lower().splitlines() 
	with open(file_nationalities, 'r') as file:
		nationalities = file.read().lower().splitlines() 
	return countries, nationalities


