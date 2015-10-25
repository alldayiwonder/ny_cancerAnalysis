import pandas as pd
import numpy as np

def read_airEmissions():

	airEmissions = pd.read_csv('data/EPA_TRI/enigma-us.gov.epa.toxic-release-inventory.ny.2013-63f546aac1daadc29b6fad5f6812568f.csv')
	# print list(airEmissions) 

	# Fields if interest: n_5_1_fugitive_air, n_5_2_stack_air
	# Trim dataframe and groupby county while aggregating fugitive and stack air emissions from all facilities within each county
	airEmissions_trim = airEmissions[['tri_facility_id','facility_name','county','n_5_1_fugitive_air','n_5_2_stack_air', 'chemical']]

	# Benzene emissions per county
	airEmissions_grouped = airEmissions_trim.groupby(['county', 'chemical'], as_index=False).aggregate(np.sum)
	airEmissions_grouped = airEmissions_grouped[airEmissions_grouped['chemical'] == 'BENZENE']
	return airEmissions_grouped

	# Merge specific chemicals with total emissions per county for correlation table

print read_airEmissions()