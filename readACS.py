import pandas as pd

def readCountyAcs():
	acsCountyFile = 'data/ACS/R11053959_SL050.csv'
	county = pd.read_csv(acsCountyFile)

	#taking fips, tot pop, male pop, age 65-74, 75-84, and 85+
	countySub = county[['Geo_FIPS', 'SE_T001_001', 'SE_T004_002', 'SE_T007_011', 'SE_T007_012', 'SE_T007_013']]
	countySub['pctMale'] = countySub['SE_T004_002'] / countySub['SE_T001_001']
	countySub['pctElderly'] = (countySub['SE_T007_011'] + countySub['SE_T007_012']+ countySub['SE_T007_013'])/ countySub['SE_T001_001']
	countySub = countySub.drop(['SE_T007_011', 'SE_T007_012', 'SE_T007_013', 'SE_T004_002'], 1)
	newCol = countySub.columns.values
	newCol[1] = 'totPop'
	countySub.columns = newCol
	countySub['countyFIPS'] = countySub['Geo_FIPS'].str[2:5]
	return acsCounty