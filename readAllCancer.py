import pandas as pd
from readFips import readFips

fips = readFips()

def readAllCancer():
	# https://health.data.ny.gov/Health/Community-Health-All-Cancer-Incidence-Age-adjusted/4wxt-6bzs
	allCancer = pd.read_csv('data/Community_Health__All_Cancer_Incidence_Age-adjusted_Rate_per_100_000_by_County_Maps__Latest_Data.csv')
	allCancer['County Name'] = allCancer['County Name'].str.upper().str.strip()
	allCanMrg = pd.merge(allCancer, fips, left_on = 'County Name', right_on = 'countyName')
	allCanMrg = allCanMrg.drop(['state', 'sCode', 'county', 'h', 'countyName'], 1)
	return allCanMrg
	