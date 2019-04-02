#!/usr/bin/python3
__author__ = 'Houcemeddine Othman'
__date__ = '2019' 

import sys 
import re 
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

inputfile = "../data/concatenated_medline.txt"
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

mytext =  parse(Medlinetxt) 

# tokenizing: separate the words and convert to a list 
tokenized_word=word_tokenize(mytext)
print( tokenized_word )
