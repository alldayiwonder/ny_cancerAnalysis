import pandas as pd
import numpy as np
from readFips import readFips
from readAllCancer import readAllCancer

fips = readFips()
allCanMrg = readAllCancer()

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
	indivCanMrgPop = pd.merge(indivCanMrg, allCanMrg[['cCode', 'Average Number of Denominator']], left_on = 'countyCode', right_on = 'cCode')

	return indivCanMrgPop
