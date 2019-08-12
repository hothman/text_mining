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
import argparse

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

def get_PMID(text):
	splitted=text.split()
	return splitted[1]

def get_title(text):
	mytext=text.split("\n")
	for line in mytext:
		if "TI  - " in line:
			title = line.split("TI  - ")[1]
			return title 

def tokenize_remove_stop_words_stemmize(text): 
	tokenized_text=word_tokenize(text.lower())
	filtered_words = [word for word in tokenized_text if word not in stopwords.words('english')]
	stemmer = SnowballStemmer("english")
	stemmed_words = [ stemmer.stem( word  ) for word in filtered_words ]
	return stemmed_words

def get_lexicon(lexicon):
	with open(lexicon, 'r') as file:
		lexicon = file.read().lower().splitlines() 
	return lexicon

def check_occurence(lexicon, corpus):
	for word in corpus: 
		if word in lexicon:
			return "PASS"

if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description="text mining for medline file format")
	parser.add_argument("--medline", help="path to medline file")
	parser.add_argument("--lexicon", help="path to the file containing the nationalities")
	args = parser.parse_args()
	assert args.medline != None, 'You must provide a medline text file'
	myMEDLINE  = open( args.medline, 'r' )
	Medlinetxt = myMEDLINE.read()
	myMEDLINE.close()
	mytext =  parse(Medlinetxt)
	mytitle = get_title(Medlinetxt)
	PMID=get_PMID(Medlinetxt)
	lexicon = get_lexicon(args.lexicon)
	tokenized_text=tokenize_remove_stop_words_stemmize(mytext)
	tokenized_title=tokenize_remove_stop_words_stemmize(mytitle)
	text_title = tokenized_text + tokenized_title
	is_pass = check_occurence(lexicon, text_title)
	print('processing PMID', PMID  )
	if is_pass == "PASS":
		print(PMID,"\t",is_pass)


