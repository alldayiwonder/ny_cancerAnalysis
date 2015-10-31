from read_airEmissions import read_airEmissions_County
from readAllCancer import mergeCancer_County
from readSmoking import readSmoking
import pandas as pd 

def main_County():
	# Import air data
	airEmissions = read_airEmissions_County()

	# Import smoking data
	#smoking = readSmoking()  # PRODUCING A WARNING

	# Import cancer data
	allCancer = mergeCancer_County()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'countyName', right_on = 'county')
	data_merged = data_merged.drop('county', 1)
	#print data_merged 
	
	print 
	print '============================ County Level Correlation Table ============================'
	return data_merged.corr()

def main_CensusBlock():
	return 'In Development'

print main_County()