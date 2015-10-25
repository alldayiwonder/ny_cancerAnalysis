import pandas as pd

def read_cancerRates():
	cancerRates = pd.read_csv('Community_Health__All_Cancer_Incidence_Age-adjusted_Rate_per_100_000_by_County_Maps__Latest_Data.csv')
	cancerRates_trim = cancerRates[['County Name', 'Percent/Rate']]
	return cancerRates_trim

