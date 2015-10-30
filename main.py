from read_airEmissions import read_airEmissions
from readAllCancer import mergeCancer
from readSmoking import readSmoking
import pandas as pd 

# Import air data
airEmissions = read_airEmissions()

# Import smoking data
smoking = readSmoking()  # PRODUCING A WARNING

# Import all-cancer data
allCancer = mergeCancer()

# Join air emission data with cancer rates data
data_merged = pd.merge(allCancer, airEmissions, left_on = 'countyName', right_on = 'county')
data_merged = data_merged.drop('county', 1)
#print data_merged 
print 
print '============================ Correlation Table ============================'
print data_merged.corr()
