import pandas as pd
import numpy as np
from read_cancerRates import read_cancerRates

#county_cancer = pd.read_csv('/Users/Steve/Github/ny_cancerAnalysis/data/NYSDOH_CancerMapping_Data_2005_2009/NYSDOH_CancerMapping_Data_2005_2009.csv')

airEmissions = pd.read_csv('/Users/Steve/Github/ny_cancerAnalysis/data/EPA_TRI/enigma-us.gov.epa.toxic-release-inventory.ny.2013-63f546aac1daadc29b6fad5f6812568f.csv')
# print list(airEmissions) 

# Fields if interest: n_5_1_fugitive_air, n_5_2_stack_air
# Trim dataframe and groupby county while aggregating fugitive and stack air emissions from all facilities within each county
airEmissions_trim = airEmissions[['tri_facility_id','facility_name','county','n_5_1_fugitive_air','n_5_2_stack_air']]
airEmissions_grouped = airEmissions_trim.groupby(['county'], as_index=False).aggregate(np.sum)
#print airEmissions_grouped

# Import cancer data
cancerRates = read_cancerRates()
cancerRates['County Name'] = map(lambda x: x.upper(), cancerRates['County Name'])  # Capitalize county names to match with other data for merge

# Join air emission data with cancer rates data
data_merged = pd.merge(cancerRates, airEmissions_grouped, left_on = 'County Name', right_on = 'county')
data_merged = data_merged.drop('county', 1)
print data_merged

print data_merged.corr()