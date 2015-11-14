import pandas as pd
import numpy as np
import requests

pd.set_option('display.width', 200)

# See https://www.census.gov/geo/reference/codes/cou.html

def readFips():
	heads = ['state', 'sCode', 'cCode', 'county', 'h']
	fips = pd.read_csv("data/st36_ny_cou.txt", names=heads, converters={'cCode': lambda x: str(x)})
	fips['countyName'] = fips['county'].str.split('County').apply(lambda x: x[0]).str.upper().str.strip()
	return fips

# print readFips()

def addGEOID_TRI():
	"""
	This function adds a 15 digit geoid code to each record in the TRI csv and outputs a new csv for read_airEmissions file
	"""
	##############
	# FILE INPUT #
	##############
	# TRI file contains 2095 records. Process takes roughly 14 minutes for this file.
	airEmissions = pd.read_csv('data/EPA_TRI/mergedData2.csv')

	# Get the Census Tract code for each facility from lat long
	# FCC API to get census block data from lat long
	# 'http://data.fcc.gov/api/block/find?format=json&latitude=[latitude]&longitude=[longitude]&showall=[true/false]'	
	airEmissions["geoid"] = np.nan
	for index, row in airEmissions.iterrows():
		try:
			#############################
			# SET LAT & LONG COLUMNS    #
			#############################

			latitude = airEmissions.values[index][2]
			longitude = airEmissions.values[index][3]
			url = 'http://data.fcc.gov/api/block/find?format=json&latitude='+str(latitude)+'&longitude='+str(longitude)+'&showall=true'
			# Get GEOID10, 15 digit version
			result = requests.get(url).json()  # Returns json as dict
			geoid = str(result['Block']['FIPS'])  # STATE+COUNTY+TRACT+BLOCK, 2+3+6+4=15 (Some blocks contain one character suffix (e.g. A))

			# Add geoid code to dataframe
			airEmissions.loc[index, "geoid"] = geoid
			
			print latitude, longitude, airEmissions.values[index][1], url
			
			##############
			# FILE OUTPUT #
			##############
			# Write to file
			airEmissions.to_csv('data/EPA_TRI/toxic-release-inventory.ny.2000.geoid.csv')
		except:
			pass
	return airEmissions

#addGEOID_TRI()

