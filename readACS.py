import pandas as pd

# geoLevel takes arguments 'county' or 'tract'
def popData(geoLevel):
	if geoLevel == 'county':
		fn = 'data/ACS/R11053959_SL050.csv'
	elif geoLevel == 'tract':
		fn = 'data/ACS/R11053959_SL140.csv'

	data = pd.read_csv(fn, dtype={'Geo_FIPS': str})
	#taking fips, tot pop, male pop, age 65-74, 75-84, and 85+, median household income
	data = data[['Geo_FIPS', 'SE_T001_001', 'SE_T004_002', 'SE_T007_011', 'SE_T007_012', 'SE_T007_013', 'SE_T057_001']]
	data['pctMale'] = data['SE_T004_002'] / data['SE_T001_001']
	data['pctElderly'] = (data['SE_T007_011'] + data['SE_T007_012']+ data['SE_T007_013'])/ data['SE_T001_001']
	data['income'] = data ['SE_T057_001']
	data = data.drop(['SE_T007_011', 'SE_T007_012', 'SE_T007_013', 'SE_T004_002', 'SE_T057_001'], 1)
	newCol = data.columns.values
	newCol[1] = 'totPop'
	data.columns = newCol
	data['countyFIPS'] = data['Geo_FIPS'].str[2:5]
	if geoLevel == 'tract':
		data['tractFIPS'] = data['Geo_FIPS'].str[2:]

<<<<<<< HEAD
	edTractData = pd.read_csv('data/ACS/education/R11060084_SL140.csv', dtype={'Geo_FIPS': str})
	# print edTractData[['SE_T025_002','SE_T150_002']]
	# print edTractData[edTractData['SE_T025_002'] != edTractData['SE_T150_002']]
	edTractData['higherEd'] = (edTractData['SE_T025_001'] - (edTractData['SE_T025_002'] + edTractData['SE_T025_003'])) / edTractData['SE_T025_001']
	edTractData['unemploy'] = edTractData['SE_T037_003'] / edTractData['SE_T037_001']
	toAdd = edTractData[['Geo_FIPS', 'higherEd', 'unemploy']]
	# print data
	# print edTractData['higherEd'].describe()
	# print edTractData['unemploy'].describe()
	merged = pd.merge(data, toAdd)
	print merged
	return merged

popData('tract')
=======

>>>>>>> origin/master
