import pandas as pd
import numpy as np
from readFips import readFips

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
	aggIndivCan
	indivCanMrg = pd.merge(aggIndivCan, fips, left_on = 'countyCode', right_on = 'cCode')
	indivCanMrg = indivCanMrg.drop(['state', 'sCode', 'cCode', 'county', 'h'], 1)

	return indivCanMrg

def mergeCancer_County():

	allCanMrg = readAllCancer_County()
	indivCanMrg = readIndivCancer_County()
	indivCanMrgPop = pd.merge(indivCanMrg, allCanMrg[['cCode', 'Average Number of Denominator']], left_on = 'countyCode', right_on = 'cCode')
	return indivCanMrgPop

def readIndivCancer_CensusBlock():
	# GEOID10 field, 12 digits: STATE (2) + COUNTY (3) + TRACT (6) + BLOCK GROUP (1)
	# Example GEOID10: 482012231001 <- Block Group 1 in Census Tract 2231 in Harris County, TX
	cancerDir = "data/NYSDOH_CancerMapping_Data_2005_2009/"
	cancerFile = "NYSDOH_CancerMapping_Data_2005_2009.csv"
	indivCancer = pd.read_csv(cancerDir+cancerFile)	
	return indivCancer

#print readIndivCancer_CensusBlock()
 