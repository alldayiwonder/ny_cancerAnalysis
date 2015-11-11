from read_airEmissions import read_airEmissions_County
from read_airEmissions import read_airEmissions_CensusTract
from readAllCancer import mergeCancer_Tract, mergeCancer_County
from readSmoking import readSmoking
from readACS import popData
from corrHeatMap import hm
import pandas as pd 
import statsmodels.formula.api as smf

pd.set_option('display.width', 200)

def main_County():
	# Import air data
	airEmissions = read_airEmissions_County()

	# Import smoking data
	smoking = readSmoking()  # PRODUCING A WARNING

	# Import cancer data
	allCancer = mergeCancer_County()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE

	# Import county level population data
	# acsCounty = popData('county')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'countyName', right_on = 'county')
	data_merged = data_merged.drop('county', 1)

	smokeMerge = pd.merge(data_merged, smoking, left_on ='countyName', right_on = 'County Name')
	testOls = pd.merge(data_merged[['observed_Total_Per100k', 'countyName']], airEmissions, left_on = 'countyName', right_on = 'county')
	testOls=testOls.drop('county',1)
	testOls=pd.merge(testOls, smoking, left_on='countyName', right_on='County Name')
	testOls.drop(['County Name', 'Location', '95% CI', 'cCode'], inplace=True, axis=1)
	# print testOls.columns.values
	# mod = smf.ols(formula='observed_Total_Per100k ~ n_5_1_fugitive_air + n_5_2_stack_air + n_5_2_stack_air_benzene + n_5_1_fugitive_air_benzene', data = testOls).fit()
	mod = smf.ols(formula='observed_Total_Per100k ~ n_5_1_fugitive_air + n_5_2_stack_air + pctSmoking', data = testOls).fit()
	print(mod.summary())

	correlation_table = smokeMerge.corr()
	correlation_table.to_csv('data/CorrelationTable/county_correlationTable.csv')
	# print correlation_table

def main_CensusTract():
	# Import air data
	airEmissions = read_airEmissions_CensusTract()

	# Import cancer data
	# allCancer = readIndivCancer_CensusTract()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE
	allCancer = mergeCancer_Tract()

	# Import smoking data
	smoking = readSmoking()  # PRODUCING A WARNING

	# Import census tract level population data
	acsTract = popData('tract')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, how='left', left_on = 'geoid11', right_on = 'geoid')
	# data_merged.fillna(0, inplace=True)
	data_merged = data_merged.drop('geoid', 1)	
	data_merged['countyCode'] = data_merged['tractFIPS'].str[:3]
	data_merged = pd.merge(data_merged, smoking, left_on = 'countyCode', right_on = 'cCode')
	data_merged = pd.merge(data_merged, acsTract, left_on = 'geoid11', right_on = 'Geo_FIPS')

	print 
	print '============= Total Cancer Incidence vs Total Air Emissions at Census Tract Level ============='
	print 
	correlation_table = data_merged.corr()
	correlation_table.to_csv('data/CorrelationTable/censusTract_correlationTable.csv')
	mod = smf.ols(formula='observed_Total_Per100k ~ airTotal + pctSmoking + pctElderly + income + higherEd + unemploy', data = data_merged).fit()
	print(mod.summary())
	print 
	print '============= Leukemia Incidence vs Fugitive Xylene Emissions at Census Tract Level ============='
	print 
	mod = smf.ols(formula='observed_Leukemia_Per100k ~ n_5_1_fugitive_air_xylene + pctSmoking + pctElderly + income', data = data_merged).fit()
	print(mod.summary())
	print
	print '============= Bladder Incidence vs Fugitive Toluene Emissions at Census Tract Level ============='
	print 
	mod = smf.ols(formula='observed_Bladder_Per100k ~ n_5_1_fugitive_air_toluene + pctSmoking + pctElderly + income', data = data_merged).fit()
	print(mod.summary())
	print
	print '============= Oral Incidence vs Fugitive Benzene Emissions at Census Tract Level ============='
	print 
	mod = smf.ols(formula='observed_Oral_Per100k ~ n_5_1_fugitive_air_benzene+ pctSmoking + pctElderly + income', data = data_merged).fit()
	print(mod.summary())

	print 
	print '============= Correlation Table Heatmap ============='
	print 
	hm(correlation_table)

main_CensusTract()
# main_County()


