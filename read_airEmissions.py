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

########################################################################################################

def read_airEmissions_CensusTract():
	"""
	Creates a dataframe where air emissions from each facility are aggregated to the Census Tract level. Air emissions data from EPA's toxic release inventory (TRI). The TRI is part of the Emergency Planning and Community Right-to-Know Act of 1986 (EPCRA). EPCRA requires companies with 10 or more employees, in certain industries, to collect and publicly disclose information about how they manufacture, process or use any of nearly 650 chemicals on a special list developed by the U.S. EPA. Companies that produce more than 25,000 pounds or handle more than 10,000 pounds of a listed toxic chemical must report.
	"""

	# Import the output from readFIPS function addGEOID_TRI. TRI file contains 2097 records.
	airEmissions = pd.read_csv('data/EPA_TRI/toxic-release-inventory.ny.2013.geoid.csv', index_col=0, dtype={'geoid': str})

	# Trim dataframe and groupby census tract and aggregate fugitive and stack air emissions 
	airEmissions_trim = airEmissions[['geoid','tri_facility_id','facility_name','county', 'n_5_1_fugitive_air','n_5_2_stack_air', 'chemical']]
	airEmissions_trim['geoid'] = airEmissions_trim['geoid'].str.slice(0,11)  # Make sure geoid does not include block
	#print airEmissions_trim

	# Get count of number of reporting facilities, result is 638 facilities
	airEmissions_facilityCount = airEmissions_trim.groupby(['tri_facility_id'], as_index=False).aggregate(np.sum)
	print 'Reporting facilities:', len(airEmissions_facilityCount)

	# Total emissions per census tract, total of 498 tracts with reporting facilities
	# This aggregation does not take into account the toxicity of individual chemicals
	airEmissions_total = airEmissions_trim.groupby(['geoid'], as_index=False).aggregate(np.sum)
	print 'Census tracts with reporting facilities:', len(airEmissions_total)
	
	# Emissions for each chemical per census tract
	airEmissions_allchemicals = airEmissions_trim.groupby(['geoid', 'chemical'], as_index=False).aggregate(np.sum)

	# List all unique chemicals with reported emissions
	airEmissions_chemicalsReported = airEmissions_allchemicals[(airEmissions_allchemicals.n_5_2_stack_air > 0) | (airEmissions_allchemicals.n_5_1_fugitive_air > 0)]  
	chemicalsReported = airEmissions_chemicalsReported['chemical'].unique().tolist()  # List of unique chemicals
	#print 'Number of unique chemicals:', len(chemicalsReported), chemicalsReported

	# Benzene emissions per census tract
	# 22 records are missing any data for benzene
	airEmissions_benzene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'BENZENE']
	airEmissions_benzene = airEmissions_benzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_benzene', 'n_5_2_stack_air': 'n_5_2_stack_air_benzene'})
	print 'Census tracts with facilities reporting benzene emissions:', len(airEmissions_benzene)
	
	# Toluene emissions per census tract
	airEmissions_toluene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'TOLUENE']
	airEmissions_toluene = airEmissions_toluene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_toluene', 'n_5_2_stack_air': 'n_5_2_stack_air_toluene'})
	print 'Census tracts with facilities reporting toluene emissions:', len(airEmissions_toluene)

	# Ethylbenzene emissions per census tract
	airEmissions_ethylbenzene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'ETHYLBENZENE']
	airEmissions_ethylbenzene = airEmissions_ethylbenzene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_ethylbenzene', 'n_5_2_stack_air': 'n_5_2_stack_air_ethylbenzene'})
	print 'Census tracts with facilities reporting ethylbenzene emissions:', len(airEmissions_ethylbenzene)

	# Xylene emissions per census tract
	airEmissions_xylene = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'XYLENE (MIXED ISOMERS)']
	airEmissions_xylene = airEmissions_xylene.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_xylene', 'n_5_2_stack_air': 'n_5_2_stack_air_xylene'})
	print 'Census tracts with facilities reporting xylene emissions:', len(airEmissions_xylene)

	# Formaldehyde emissions per census tract
	airEmissions_formaldehyde = airEmissions_allchemicals[airEmissions_allchemicals['chemical'] == 'FORMALDEHYDE']
	airEmissions_formaldehyde = airEmissions_formaldehyde.rename(columns={'n_5_1_fugitive_air': 'n_5_1_fugitive_air_formaldehyde', 'n_5_2_stack_air': 'n_5_2_stack_air_formaldehyde'})
	print 'Census tracts with facilities reporting formaldehyde emissions:', len(airEmissions_formaldehyde)

	# Merge the aggregation of each specific chemical with the total emissions for the main file
	airEmissions_total['airTotal'] = airEmissions_total['n_5_2_stack_air'] + airEmissions_total['n_5_1_fugitive_air'] 

	data_merged_benz = pd.merge(airEmissions_total, airEmissions_benzene, how='outer')
	data_merged_benz = data_merged_benz.drop('chemical', 1)
	data_merged_benz['benzeneTotal'] = data_merged_benz['n_5_1_fugitive_air_benzene'] + data_merged_benz['n_5_2_stack_air_benzene'] 

	data_merged_tol = pd.merge(data_merged_benz, airEmissions_toluene, how='outer')

	data_merged_tol = data_merged_tol.drop('chemical', 1)
	data_merged_tol['tolueneTotal'] = data_merged_tol['n_5_1_fugitive_air_toluene'] + data_merged_tol['n_5_2_stack_air_toluene'] 
	
	data_merged_ebenz = pd.merge(data_merged_tol, airEmissions_ethylbenzene, how='outer')
	data_merged_ebenz = data_merged_ebenz.drop('chemical', 1)
	data_merged_ebenz['ebenzTotal'] = data_merged_ebenz['n_5_1_fugitive_air_ethylbenzene'] + data_merged_ebenz['n_5_2_stack_air_ethylbenzene'] 
	
	data_merged_xylene = pd.merge(data_merged_ebenz, airEmissions_xylene, how='outer')
	data_merged_xylene = data_merged_xylene.drop('chemical', 1)
	data_merged_xylene['xyleneTotal'] = data_merged_xylene['n_5_1_fugitive_air_xylene'] + data_merged_xylene['n_5_2_stack_air_xylene'] 

	data_merged_formaldehyde = pd.merge(data_merged_xylene, airEmissions_formaldehyde, how='outer')
	data_merged_formaldehyde = data_merged_formaldehyde.drop('chemical', 1)
	data_merged_formaldehyde['formaldehydeTotal'] = data_merged_formaldehyde['n_5_1_fugitive_air_formaldehyde'] + data_merged_formaldehyde['n_5_2_stack_air_formaldehyde'] 


	return data_merged_formaldehyde  #Need to change to formaldehyde, but fix error first

#read_airEmissions_County()
read_airEmissions_CensusTract()





