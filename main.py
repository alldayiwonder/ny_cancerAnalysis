from read_cancerRates import read_cancerRates
from read_airEmissions import read_airEmissions
import pandas as pd 

# Import cancer data
cancerRates = read_cancerRates()
cancerRates['County Name'] = map(lambda x: x.upper(), cancerRates['County Name'])  # Capitalize county names to match with other data for merge

# Import air data
airEmissions = read_airEmissions()

# Join air emission data with cancer rates data
data_merged = pd.merge(cancerRates, airEmissions, left_on = 'County Name', right_on = 'county')
data_merged = data_merged.drop('county', 1)
print data_merged

print data_merged.corr()