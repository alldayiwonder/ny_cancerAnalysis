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

	# Toluene emissions per county
	airEmissions_toluene = airEmissions_trim.groupby(['county', 'chemical'], as_index=False).aggregate(np.sum)
	airEmissions_toluene = airEmissions_toluene[airEmissions_toluene['chemical'] == 'TOLUENE']
	airEmissions_toluene = airEmissions_toluene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_toluene', 'n_5_2_stack_air': 'n_5_2_stack_air_toluene'})

	# Merge the aggregation of each specific chemical with the total emissions per county for the main file
	data_merged_benz = pd.merge(airEmissions_total, airEmissions_benzene)
	data_merged_benz = data_merged_benz.drop('chemical', 1)
	data_merged = pd.merge(data_merged_benz, airEmissions_toluene)
	data_merged = data_merged.drop('chemical', 1)

	return data_merged

def read_airEmissions_CensusTract():
	"""
	Creates a dataframe where air emissions from each facility are aggregated to the Census Tract level. Air emissions data from EPA's toxic release inventory (TRI). The TRI is part of the Emergency Planning and Community Right-to-Know Act of 1986 (EPCRA). EPCRA requires companies with 10 or more employees, in certain industries, to collect and publicly disclose information about how they manufacture, process or use any of nearly 650 chemicals on a special list developed by the U.S. EPA. Companies that produce more than 25,000 pounds or handle more than 10,000 pounds of a listed toxic chemical must report.
	"""

	# Import the output from readFIPS function addGEOID_TRI. TRI file contains 2095 records.
	airEmissions = pd.read_csv('data/EPA_TRI/toxic-release-inventory.ny.2013.geoid.csv', index_col=0, dtype={'geoid': str})

	# Trim dataframe and groupby census tract and aggregate fugitive and stack air emissions 
	airEmissions_trim = airEmissions[['geoid','tri_facility_id','facility_name','county', 'n_5_1_fugitive_air','n_5_2_stack_air', 'chemical']]
	airEmissions_trim['geoid'] = airEmissions_trim['geoid'].str.slice(0,11)  # Make sure geoid does not include block
	
	# Total emissions per census tract, total of 498 tracts in TRI data set
	airEmissions_total = airEmissions_trim.groupby(['geoid'], as_index=False).aggregate(np.sum)
	
	# Emissions for each chemical per census tract
	airEmissions_allchemicals = airEmissions_trim.groupby(['geoid', 'chemical'], as_index=False).aggregate(np.sum)
	
	# Optional code
	# Finds only those records where stack and fugitive emissions are greater than arbitray value
	airEmissions_allchemicals = airEmissions_allchemicals[(airEmissions_allchemicals.n_5_2_stack_air > 0) | (airEmissions_allchemicals.n_5_1_fugitive_air > 0)]  
	
	# List unique chemicals 
	allchemicals = airEmissions_allchemicals['chemical'].unique().tolist()  # List of unique chemicals
	#print 'Number of unique chemicals:', len(allchemicals)

	# Benzene emissions per census tract
	airEmissions_benzene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'BENZENE']
	airEmissions_benzene = airEmissions_benzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_benzene', 'n_5_2_stack_air': 'n_5_2_stack_air_benzene'})

	# Toluene emissions per census tract
	airEmissions_toluene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'TOLUENE']
	airEmissions_toluene = airEmissions_toluene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_toluene', 'n_5_2_stack_air': 'n_5_2_stack_air_toluene'})

	# Ethylbenzene emissions per census tract
	airEmissions_ethylbenzene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'ETHYLBENZENE']
	airEmissions_ethylbenzene = airEmissions_ethylbenzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_ethylbenzene', 'n_5_2_stack_air': 'n_5_2_stack_air_ethylbenzene'})

	# Xylene emissions per census tract
	airEmissions_xylene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'XYLENE (MIXED ISOMERS)']
	airEmissions_xylene = airEmissions_xylene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_xylene', 'n_5_2_stack_air': 'n_5_2_stack_air_xylene'})

	# Merge the aggregation of each specific chemical with the total emissions per county for the main file
	data_merged_benz = pd.merge(airEmissions_total, airEmissions_benzene)
	data_merged_benz = data_merged_benz.drop('chemical', 1)
	data_merged_tol = pd.merge(data_merged_benz, airEmissions_toluene)
	data_merged_tol = data_merged_tol.drop('chemical', 1)
	data_merged_ebenz = pd.merge(data_merged_tol, airEmissions_ethylbenzene)
	data_merged_ebenz = data_merged_ebenz.drop('chemical', 1)
	data_merged_xylene = pd.merge(data_merged_ebenz, airEmissions_xylene)
	data_merged_xylene = data_merged_xylene.drop('chemical', 1)
	return data_merged_xylene

#read_airEmissions_County()
#read_airEmissions_CensusTract()




