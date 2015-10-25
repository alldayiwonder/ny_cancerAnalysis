import pandas as pd
from readFips import readFips

fips = readFips()

def readSmoking():
	smokData = pd.read_csv('data/PA__Percentage_of_Cigarette_Smoking_Among_Adults_Map.csv')
	subSmok = smokData[list([smokData.columns[6], smokData.columns[9], smokData.columns[10], smokData.columns[-1]])]
	subSmok['County Name'] = subSmok['County Name'].str.upper().str.strip()
	smokMrg = pd.merge(subSmok, fips, left_on = 'County Name', right_on = 'countyName')
	smokMrg = smokMrg.drop(['state', 'sCode', 'county', 'h', 'countyName'], 1)
	return smokMrg