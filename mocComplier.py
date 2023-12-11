import fnmatch
import os
import pandas as pd
import sys
import re
import sys

def main():
	#1) Make a list of relevent Major Oxide Composition (MOC) files
	moc_path_list = findFiles()

	#1.1) Print out a list of the files in order
	#files_list = listFiles(moc_path_list)

	#2) Create a DF of all the MOC data
	df_moc = createDataFrameMoc(moc_path_list)

	#3) Process the DF for compatibility with The Sequencer
	df_moc = processMOC(df_moc)
	
	#4) Now we ouput the MOC df & a list of compounds to .csv
	outputCSV(df_moc)

def findFiles():
	# Function recusivly looks through specified directory for relevent files
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	else:
		directory = str(input("Abolsute input path: "))

	matches = []
	for root, dirnames, filenames in os.walk(directory):
		for filename in fnmatch.filter(filenames, 'moc*.csv'):
			matches.append(os.path.join(root, filename))
	# The following sorts matches based on "human sorting" (letters and nums matter)
	matches.sort(key=natural_keys)
	
	return matches

def listFiles(list_paths):
	df_sum_files = pd.DataFrame()
	
	for i in range(len(list_paths)):
		df_temp = pd.read_csv(list_paths[i], low_memory=False)
		df_files = df_temp.iloc[6:, 0]
		df_sum_files = pd.concat([df_sum_files, df_files], axis=0, ignore_index=True)

	df_sum_files = df_sum_files[0].str.lower()
	#df_sum_files.to_csv("mocFilesInOrder.csv", header=False, index=False)
	return df_sum_files

def createDataFrameMoc(list_paths):
	# Function complies all MOC columns from list_path and returns them as Pandas DataFrame
	df_sum = pd.DataFrame()
	
	for i in range(len(list_paths)):
		print(i, list_paths[i])
		# df_temp will end up being 9 columns for MOC data from 1 file
		df_temp = pd.read_csv(list_paths[i], low_memory=False)
		df_temp = df_temp.loc[:, ["SiO2", "TiO2", "Al2O3", "FeOT", "MgO", "CaO", "Na2O", "K2O", "MnO"]]
		df_temp.drop(range(0,6), inplace=True) # removes blank rows
		df_temp = df_temp.astype(float)
		df_sum = pd.concat([df_sum, df_temp], axis=0, ignore_index=True)

	return df_sum

def processMOC(df):
	# Function ensures data is comptable with The Sequencer
	# Corrects: dtype, all cell vales > 1, round 2 decimal places
	df = df.astype(float)
	min_value = df.min(numeric_only=True).min()
	if min_value <= 0:
		abs_min = min_value * -1
		df = df + (abs_min + 1)
	else:
		pass

	df = round(df, 2)
	return df	

def atoi(text):
	# Function helps sort / organize the list of file dirs
	return int(text) if text.isdigit() else text

def natural_keys(text):
	# Function helps sort / organize the list of file dirs
	return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def outputCSV(df_moc):
	# Function outputs MOC data and Compounds to .csv files
	if len(sys.argv) > 2:
		dir_moc = sys.argv[2]
	else:
		dir_moc = str(input("Name of Compiled Moc File (include .csv): "))
	if len(sys.argv) > 3:
		dir_compounds = sys.argv[3]
	else:
		dir_compounds = str(input("Name of Oxide Numbers (include .csv): "))

	lst_compounds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	df_compounds = pd.DataFrame(lst_compounds)
	df_compounds = df_compounds.astype(float)

	df_moc.to_csv(dir_moc, index=False, header=False)
	df_compounds.to_csv(dir_compounds, index=False, header=False)


main()
