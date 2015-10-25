from read_cancerRates import read_cancerRates
from read_airEmissions import read_airEmissions
from readSmoking import readSmoking
from readAllCancer import readAllCancer
from readIndivCancer import readIndivCancer
import pandas as pd 

# Import cancer data
cancerRates = read_cancerRates()
# Capitalize county names to match with other data for merge
cancerRates['County Name'] = map(lambda x: x.upper(), cancerRates['County Name'])  

# Import air data
airEmissions = read_airEmissions()

# Import smoking data
smoking = readSmoking()

# Import all-cancer data
allCancer = readAllCancer()

# Import individual cancer data
indivCancer = readIndivCancer()

# Join air emission data with cancer rates data
data_merged = pd.merge(cancerRates, airEmissions, left_on = 'County Name', right_on = 'county')
data_merged = data_merged.drop('county', 1)
print data_merged 
print 
print '============================ Correlation Table ============================'
print data_merged.corr()