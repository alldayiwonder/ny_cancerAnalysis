import pandas as pd
import numpy as np
from readFips import readFips

fips = readFips()

def readAllCancer():
	# https://health.data.ny.gov/Health/Community-Health-All-Cancer-Incidence-Age-adjusted/4wxt-6bzs
	allCancer = pd.read_csv('data/Community_Health__All_Cancer_Incidence_Age-adjusted_Rate_per_100_000_by_County_Maps__Latest_Data.csv')
	allCancer['County Name'] = allCancer['County Name'].str.upper().str.strip()
	allCanMrg = pd.merge(allCancer, fips, left_on = 'County Name', right_on = 'countyName')
	allCanMrg = allCanMrg.drop(['state', 'sCode', 'county', 'h', 'countyName'], 1)
	allCanMrg = allCanMrg[['County Name', 'Percent/Rate', 'cCode', 'Average Number of Denominator']]
	return allCanMrg

def readIndivCancer():
	# individual cancer data:
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

def mergeCancer():

	allCanMrg = readAllCancer()
	indivCanMrg = readIndivCancer()
	indivCanMrgPop = pd.merge(indivCanMrg, allCanMrg[['cCode', 'Average Number of Denominator']], left_on = 'countyCode', right_on = 'cCode')
	return indivCanMrgPop

 