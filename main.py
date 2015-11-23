from read_airEmissions import read_airEmissions_County
from read_airEmissions import read_airEmissions_CensusTract
from readAllCancer import mergeCancer_Tract, mergeCancer_County
from readSmoking import readSmoking
from readACS import popData
from readCancerRisk import read_cancerRisk_CensusTract
from corrHeatMap import hm
import pandas as pd 
import statsmodels.formula.api as smf

pd.set_option('display.width', 200)

def main_County():
	# Import air data
	airEmissions = read_airEmissions_County()

	# Import smoking data
	smoking = readSmoking()   

	# Import cancer data
	allCancer = mergeCancer_County() 

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
	# mod = smf.ols(formula='observed_Total_Per100k ~ n_5_1_fugitive_air + n_5_2_stack_air + pctSmoking', data = testOls).fit()
	# print(mod.summary())

	correlation_table = smokeMerge.corr()
	correlation_table.to_csv('data/CorrelationTable/county_correlationTable.csv')
	# print correlation_table

###################################################################################################

def main_CensusTract():
	# Import air data
	airEmissions = read_airEmissions_CensusTract()

	# Import cancer data
	# allCancer = readIndivCancer_CensusTract()  
	allCancer = mergeCancer_Tract()

	# Import smoking data
	smoking = readSmoking()   

	# Import census tract level population data
	acsTract = popData('tract')

	# Import cancer risk data
	cancerRisk = read_cancerRisk_CensusTract()

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, how='left', left_on = 'geoid11', right_on = 'geoid')
	data_merged.fillna(0, inplace=True)  # To avoid losing those tracts in model with smoking and demographic data but no chemical releases 
	data_merged = data_merged.drop('geoid', 1)	
	data_merged['countyCode'] = data_merged['tractFIPS'].str[:3]
	data_merged = pd.merge(data_merged, smoking, left_on = 'countyCode', right_on = 'cCode')
	data_merged = pd.merge(data_merged, acsTract, left_on = 'geoid11', right_on = 'Geo_FIPS')
	data_merged = pd.merge(data_merged, cancerRisk, left_on = 'Geo_FIPS', right_on = 'GEOID')

	# Produce correlation table
	correlation_table = data_merged.corr()
	correlation_table.to_csv('data/CorrelationTable/censusTract_correlationTable.csv')

	cancer_list = ['observed_Bladder_Per100k', 'observed_Bone_Per100k',	'observed_Brain_Per100k', 
	'observed_Breast_Per100k', 'observed_Colorectal_Per100k','observed_Esophagus_Per100k', 'observed_Kidney_Per100k', 
	'observed_Larynx_Per100k', 'observed_Leukemia_Per100k',	'observed_Liver_Per100k', 'observed_Lung_Per100k',	
	'observed_Mesothelioma_Per100k', 'observed_NHL_Per100k', 'observed_Nasal_Per100k', 'observed_Oral_Per100k',	
	'observed_Other_Per100k', 'observed_Ovary_Per100k',	'observed_Pancreas_Per100k', 'observed_Prostate_Per100k',	
	'observed_Soft_Tissue_Per100k',	'observed_Stomach_Per100k',	'observed_Testis_Per100k', 'observed_Thyroid_Per100k',	
	'observed_Uterus_Per100k', 'observed_Total_Per100k']

	chemical_list = ['n_5_1_fugitive_air', 'n_5_2_stack_air', 'airTotal', 'n_5_1_fugitive_air_benzene',
	'n_5_2_stack_air_benzene', 'benzeneTotal', 'n_5_1_fugitive_air_toluene', 'n_5_2_stack_air_toluene', 
	'tolueneTotal', 'n_5_1_fugitive_air_ethylbenzene', 'n_5_2_stack_air_ethylbenzene', 'ethylbenzeneTotal',
	'n_5_1_fugitive_air_xylene', 'n_5_2_stack_air_xylene', 'xyleneTotal', 'n_5_1_fugitive_air_formaldehyde',
	'n_5_2_stack_air_formaldehyde', 'formaldehydeTotal', 'BTEX_fugitive', 'BTEX_stack', 'BTEX_total', 
	'n_5_1_fugitive_air_dioxin', 'n_5_2_stack_air_dioxin', 'dioxinTotal']

	for chemical in chemical_list:
		with open('data/Regression/'+chemical+'.csv', 'w') as f:
			# columns = ['Cancer', 'Coefficient', 'p-Value', 'Std. Error', 'Adj. R']
			# result_df = pd.DataFrame(index=columns)
			for cancer in cancer_list:
				mod = smf.ols(formula=cancer+' ~ '+chemical+' + \
					pctSmoking + pctElderly + income + higherEd + unemploy', data = data_merged).fit(cov_type='HC0')
				 
				result_df = pd.DataFrame({
					'Cancer': cancer,
					'Coefficient': mod.params.apply(lambda x: round(x, 3)),
		            'p-Value': mod.pvalues.apply(lambda x: round(x, 3)),
		            'Std. Error': mod.bse.astype(int),
		            'Adj. R': round(mod.rsquared_adj, 3)})

				# Coefficient for air emission feature is mod.params[1]
				
				if mod.params[1] > 1.0:
					print 'Cancer and pollutant combination with Coefficient > 1:'
					print mod.params[1], mod.pvalues[1], cancer, chemical  

				result_df.to_csv(f)

	# Test model
	mod = smf.ols(formula='observed_Kidney_Per100k ~ n_5_1_fugitive_air_dioxin + \
	pctSmoking + pctElderly + income + higherEd + unemploy', data = data_merged).fit(cov_type='HC0')
	print mod.summary()
	# Correlation Table Heat Map
	hm(correlation_table)

main_CensusTract()


