import pandas as pd
import numpy as np
from readFips import readFips
from readACS import popData

#pd.set_option('display.width', 100)

fips = readFips()


def readAllCancer_County():
	# Total cancer rate, age adjusted
	# Data from https://health.data.ny.gov/Health/Community-Health-All-Cancer-Incidence-Age-adjusted/4wxt-6bzs
	allCancer = pd.read_csv('data/Community_Health__All_Cancer_Incidence_Age-adjusted_Rate_per_100_000_by_County_Maps__Latest_Data.csv')
	allCancer['County Name'] = allCancer['County Name'].str.upper().str.strip()
	allCanMrg = pd.merge(allCancer, fips, left_on = 'County Name', right_on = 'countyName')
	allCanMrg = allCanMrg.drop(['state', 'sCode', 'county', 'h', 'countyName'], 1)
	allCanMrg = allCanMrg[['County Name', 'Percent/Rate', 'cCode', 'Average Number of Denominator']]
	return allCanMrg

def readIndivCancer_County():
	# Individual cancer data
	# Counts of newly diagnosed cancer among New York State residents
	cancerDir = "data/NYSDOH_CancerMapping_Data_2005_2009/"
	cancerFile = "NYSDOH_CancerMapping_Data_2005_2009.csv"
	indivCancer = pd.read_csv(cancerDir+cancerFile)

	indivCancer['countyCode'] = indivCancer['geoid10'].str.slice(2,5)
	limited = indivCancer[[indivCancer.columns[-1]] + [indivCancer.columns[0]] + list(indivCancer.columns[1:26])]
	ls = list(limited.columns.values)[2:]
	byCounty = limited.groupby('countyCode')
	aggIndivCan = pd.DataFrame()
	for i in ls:
	    aggIndivCan[i] = byCounty[i].aggregate(np.sum)
	aggIndivCan = aggIndivCan.reset_index()
	indivCanMrg = pd.merge(aggIndivCan, fips, left_on = 'countyCode', right_on = 'cCode')
	indivCanMrg = indivCanMrg.drop(['state', 'sCode', 'cCode', 'county', 'h'], 1)
	return indivCanMrg

def mergeCancer_County():

	# allCanMrg = readAllCancer_County()
	acsCounty = popData('county')
	indivCanMrg = readIndivCancer_County()
	indivCanMrgPop = pd.merge(indivCanMrg, acsCounty[['countyFIPS', 'totPop']], left_on = 'countyCode', right_on = 'countyFIPS')
	canCols = indivCanMrgPop.columns.values[1:-3]
	for i in canCols:
		indivCanMrgPop[i+'-Per100k'] = indivCanMrgPop[i]*100000/indivCanMrgPop['totPop']
	indivCanMrgPop.drop(canCols, inplace=True,axis=1)
	newCols = [x for x in list(indivCanMrgPop.columns.values) if x not in ['countyCode', 'countyFIPS', 'totPop', 'countyName']]
	for x in ['totPop', 'countyName', 'countyFIPS']:
		newCols.insert(0, x)
	indivCanMrgPop = indivCanMrgPop[newCols]
	print indivCanMrgPop.columns.values
	return indivCanMrgPop

def readIndivCancer_CensusTract():
	# GEOID10 field, 12 digits: STATE (2) + COUNTY (3) + TRACT (6) + BLOCK GROUP (1)
	# Example GEOID10: 482012231001 <- Block Group 1 in Census Tract 2231 in Harris County, TX
	# Need to slice the block digit off of GEOID10 field to get census tract only 
	cancerDir = "data/NYSDOH_CancerMapping_Data_2005_2009/"
	cancerFile = "NYSDOH_CancerMapping_Data_2005_2009.csv"
	indivCancer = pd.read_csv(cancerDir+cancerFile)	
	indivCancer['geoid10'] = indivCancer['geoid10'].str.slice(0,11)
	indivCancer = indivCancer.groupby(['geoid10'], as_index=False).aggregate(np.sum)
	#print indivCancer
	return indivCancer

mergeCancer_County()
