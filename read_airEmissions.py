import pandas as pd

#county_cancer = pd.read_csv('/Users/Steve/Github/ny_cancerAnalysis/data/NYSDOH_CancerMapping_Data_2005_2009/NYSDOH_CancerMapping_Data_2005_2009.csv')

airEmissions = pd.read_csv('/Users/Steve/Github/ny_cancerAnalysis/data/EPA_TRI/enigma-us.gov.epa.toxic-release-inventory.ny.2013.csv')
print airEmissions.describe()
