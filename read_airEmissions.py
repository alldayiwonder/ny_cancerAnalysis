import pandas as pd
import numpy as np
import requests 

pd.set_option('display.width', 200)

def read_airEmissions_County():
	"""
	Creates a dataframe where air emissions from each facility are aggregated to the county level
	"""

	airEmissions = pd.read_csv('data/EPA_TRI/enigma-us.gov.epa.toxic-release-inventory.ny.2013-63f546aac1daadc29b6fad5f6812568f.csv')
	# print list(airEmissions) 

	# Fields of interest: n_5_1_fugitive_air, n_5_2_stack_air
	# Trim dataframe and groupby county while aggregating fugitive and stack air emissions from all facilities within each county
	airEmissions_trim = airEmissions[['tri_facility_id','facility_name','county','n_5_1_fugitive_air','n_5_2_stack_air', 'chemical']]

	# Total emissions per county
	airEmissions_total = airEmissions_trim.groupby(['county'], as_index=False).aggregate(np.sum)

	# Benzene emissions per county
	airEmissions_benzene = airEmissions_trim.groupby(['county', 'chemical'], as_index=False).aggregate(np.sum)
	airEmissions_benzene = airEmissions_benzene[airEmissions_benzene['chemical'] == 'BENZENE']
	airEmissions_benzene = airEmissions_benzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_benzene', 'n_5_2_stack_air': 'n_5_2_stack_air_benzene'})

	# Merge the aggregation of each specific chemical with the total emissions per county for the main file
	data_merged = pd.merge(airEmissions_total, airEmissions_benzene)
	data_merged = data_merged.drop('chemical', 1)
	return data_merged

def read_airEmissions_CensusBlock():
	"""
	Creates a dataframe where air emissions from each facility are aggregated to the Census Block level
	"""

	# Import the output from readFIPS function addGEOID_TRI. TRI file contains 2095 records.
	airEmissions = pd.read_csv('data/EPA_TRI/toxic-release-inventory.ny.2013.geoid.csv', index_col=0, dtype={'geoid': str})

	# Trim dataframe and groupby census tract block and aggregate fugitive and stack air emissions 
	airEmissions_trim = airEmissions[['geoid','tri_facility_id','facility_name','county', 'n_5_1_fugitive_air','n_5_2_stack_air', 'chemical']]
	airEmissions_trim['geoid'] = airEmissions_trim['geoid'].str.slice(0,12)
	
	# Total emissions per census tract block
	airEmissions_total = airEmissions_trim.groupby(['geoid'], as_index=False).aggregate(np.sum)

	# Benzene emissions per census tract block
	airEmissions_benzene = airEmissions_trim.groupby(['geoid', 'chemical'], as_index=False).aggregate(np.sum)
	airEmissions_benzene = airEmissions_benzene[airEmissions_benzene['chemical'] == 'BENZENE']
	airEmissions_benzene = airEmissions_benzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_benzene', 'n_5_2_stack_air': 'n_5_2_stack_air_benzene'})

	# Merge the aggregation of each specific chemical with the total emissions per county for the main file
	data_merged = pd.merge(airEmissions_total, airEmissions_benzene)
	data_merged = data_merged.drop('chemical', 1)
	return data_merged

#print read_airEmissions_CensusBlock()





