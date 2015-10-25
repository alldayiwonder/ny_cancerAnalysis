import pandas as pd

# https://www.census.gov/geo/reference/codes/cou.html

def readFips():
	heads = ['state', 'sCode', 'cCode', 'county', 'h']
	fips = pd.read_csv("data/st36_ny_cou.txt", names=heads, converters={'cCode': lambda x: str(x)})
	fips['countyName'] = fips['county'].str.split('County').apply(lambda x: x[0]).str.upper().str.strip()
	return fips