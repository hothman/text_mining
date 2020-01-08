#!/usr/bin/python3
__author__ = 'Houcemeddine Othman'
__date__ = '2019' 
__email__='houcemoo@gmail.com'

"""
Extract country, date and molecule type from 
genbank file
"""
import argparse

def read_gb(gb_file):
	with open(gb_file, 'r') as inputfile:
		genbankfile = inputfile.readlines()
	return genbankfile

def parse_gb(genbank):
	country=""
	first_line = genbank[0].split()
	molecule = first_line[4]
	year = first_line[-1].split('-')[2]
	for line in genbank:
		if "/country=" in line:
			if ":" in line:
				country = line.split(":")[0].split("\"")[-1]
			else:
				country =  line.split("\"")[-2] 

	if country =="":
		country = "NO_COUNTRY"

	return year, molecule, country

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Extract country, date and molecule type from genbank file")
	parser.add_argument("--genbank", help="path to genbank file")
	args = parser.parse_args()

	#myfile = read_gb("../data/MN293036.1.gb")
	myfile = read_gb(args.genbank)
	data = parse_gb(myfile)
	print(data[2],"\t",data[1],"\t", data[0] )
