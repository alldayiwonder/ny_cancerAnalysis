from read_airEmissions import read_airEmissions_County
from read_airEmissions import read_airEmissions_CensusTract
from readAllCancer import mergeCancer_County
from readAllCancer import readIndivCancer_CensusTract
from readSmoking import readSmoking
from readAcs import popData
import pandas as pd 

pd.set_option('display.width', 200)

def main_County():
	# Import air data
	airEmissions = read_airEmissions_County()

	# Import smoking data
	#smoking = readSmoking()  # PRODUCING A WARNING

	# Import cancer data
	allCancer = mergeCancer_County()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE

	# Import county level population data
	acsCounty = popData('county')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'countyName', right_on = 'county')
	data_merged = data_merged.drop('county', 1)
	#print data_merged 
	
	print 
	print '============================ County Level Correlation Table ============================'
	print data_merged.corr()

def main_CensusTract():
	# Import air data
	airEmissions = read_airEmissions_CensusTract()

	# Import cancer data
	allCancer = readIndivCancer_CensusTract()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE

	# Import census tract level population data
	acsTract = popData('tract')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'geoid10', right_on = 'geoid')
	data_merged = data_merged.drop('geoid', 1)	
	#print data_merged

	print 
	print '============================ County Level Correlation Table ============================'
	print data_merged.corr()

main_CensusTract()


