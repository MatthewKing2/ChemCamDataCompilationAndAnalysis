import fnmatch
import os
import pandas as pd
import sys
import re
import sys

def main():
	#1) Find .csv files with "ccs"
	ccs_path_list = findFiles()
	
	#1.1) Print out list of all the files in order
	#file_list = listFiles(ccs_path_list)

	#2) Now we will create a DF of the "average" radiance column (& cache as we go)
	df_radiance = createDataFrameRadiance(ccs_path_list)

	#3) Now we will create a DF of the wavelengths (col 0)
	df_wave = createDataFrameWavelength(ccs_path_list)
	
	#4) Now we will "process" df_radiance so it is comptible w/ The Sequencer
	df_radiance = processRadiance(df_radiance)

	#5) Lastly, output both DF to .csv files
	outputCSV(df_radiance, df_wave)

def findFiles():
	# Function recursivly looks through specified directory for relevent files
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	else:
		directory = str(input("Input directory (where CCS and MOC files live): "))

	matches = []
	for root, dirnames, filenames in os.walk(directory):
		for filename in fnmatch.filter(filenames, 'cl5_*ccs*.csv'):
			matches.append(os.path.join(root, filename))
	# The following sorts matches based on "human sorting" (letters & nums matter)
	matches.sort(key=natural_keys)

	return matches

def listFiles(list_paths):
	# Funtion returns a Pandas DataFrame (df) of the files (not paths)
	files = []
	for path in list_paths:
		if "/" in path:
			last_slash = path.rindex('/')
			files.append(path[last_slash+1:])
		else:
			files.append(path)
	df = pd.DataFrame(files)
	#df.to_csv('radianceFilesInOrderIndex.csv', header=False)
	return df




def createDataFrameRadiance(list_paths):
	# Function complies all avgRadiance columns from list_paths and returns them as Pandas DataFrame
	df_sum = pd.DataFrame()
	if len(sys.argv) > 2:
		start_file = int(sys.argv[2])
	else:
		start_file = int(input("Start file (0 for beginning): "))
	if len(sys.argv) > 3:
		cache_num = int(sys.argv[3])
	else:
		cache_num = int(input("Cache every x files: "))
	
	for i in range(len(list_paths[start_file:])):
		rel_i = i+start_file
		print(rel_i, list_paths[rel_i])

		# df_temp will end up being the avg radiance column from 1 specific .csv
		df_temp = pd.read_csv(list_paths[rel_i], low_memory=False)
		# The following block of code finds the number of shots taken (# irrelevent cols)
		num_shots = str(df_temp["# PRODUCER_ID = cron "].loc[df_temp.index[11]])
		num_shots = num_shots.replace(" ", "") #This removes all spaces
		num_shots = int(num_shots[8:])
		# The following removes all of the columns except the avg radiance	
		df_temp.drop(columns=df_temp.columns[0:num_shots+2], inplace=True)
		# The following removes all irrelivent rows & casts data to float saving RAM
		df_temp.drop(range(0,16), inplace=True) #removes blank rows 
		df_temp = df_temp.astype(float)

		# The following adds the df_temp to the df_sum as a column and prints RAM usage
		df_sum = pd.concat([df_sum, df_temp], axis=1, ignore_index=True)

		# Calls the cache function to save 
		if rel_i%cache_num == 0 and rel_i != 0:
			cacheRadiance(df_sum, rel_i)

	return df_sum

def createDataFrameWavelength(list_paths):
	# Function takes wavelength column from 1 file and returns it as Pandas DataFrame
	df_wave = pd.read_csv(list_paths[0], usecols = [0])
	df_wave.drop(range(0,16), inplace=True)
	df_wave = df_wave.reset_index(drop=True)
	df_wave.rename(columns={"# PRODUCER_ID = cron ": "wave"}, inplace=True)
	df_wave = df_wave.astype(float)

	return df_wave

def cacheRadiance(df, index):
	# Saves a backup copy of radiance dataframe to cache folder
	# The following determins the indent of print statments in (#) and prints size of df
	num_indent = len(str(index))
	indent = "#" * num_indent
	print(indent + " Size of cache (Megabytes):", "%.3f" % (sys.getsizeof(df)/1000000))
	# The following makes a cache folder if it DNE
	cache_path = "avgRadianceCache"
	cache_exist = os.path.exists(cache_path)
	if not cache_exist:
		print(indent + " Creating: avgRadianceCache")
		os.makedirs(cache_path)
	# The following removes redundent cached files
	file_name = cache_path + "/avgRadianceTo" + str(index) + ".csv"
	file_exist = os.path.exists(file_name)
	if file_exist:
		print(indent + " Removing redundent file:", file_name)
		os.remove(file_name)
	# The following process the df and outputs it to cache folder
	df = processRadiance(df)
	print(indent + " Saving cache:", index)
	df.to_csv(file_name, index=False, header=False)

def processRadiance(df):
	# Function ensures data is compatable with The Sequencer
	# Corrects: index, dtype, row/col, & all cell values > 1
	df = df.reset_index(drop=True)
	df = df.astype(float) # Redenundent but keeping
	df = df.transpose() # Swaps the rows & columns so now wavelen would be column header

	# The following ensures all cell values are >1
	min_value = df.min(numeric_only=True).min()
	if min_value <= 0:
		abs_min = min_value * -1
		df = df + (abs_min + 1)
	else:
		pass

	return df	

def atoi(text):
	# Function helps sort / organize the list of file directories
	return int(text) if text.isdigit() else text

def natural_keys(text):
	# Function helps sort / organize the list of file directories
	return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def outputCSV(radiance_df, wave_df):
	# Function ouputs Radiance and Wave DataFrames to .csv files
	if len(sys.argv) > 4:
		dir_radiance = sys.argv[4]
	else:
		dir_radiance = str(input("Name of Compiled Avgerage Radiance File (include .csv): "))
	if len(sys.argv) > 5:
		dir_wave = sys.argv[5]
	else:
		dir_wave = str(input("Name of Wavelengths File (include .csv): "))
	
	radiance_df.to_csv(dir_radiance, index=False, header=False)
	wave_df.to_csv(dir_wave, index=False, header=False)

main()
