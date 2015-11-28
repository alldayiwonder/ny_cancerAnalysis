import pandas as pd 

pd.set_option('display.width', 150)

def read_cancerRisk_CensusTract():
	"""
	Creates a dataframe from cancer risk data as obtained from EPA's National Air Toxics Assessment (NATA).
	"""
	cancerRisk = pd.read_csv('data/EPA_NATA/US_NATA05_NY.csv')
	cancerRisk["TRACT"] = cancerRisk.TRACT.map("{:06}".format)

	cancerRisk["GEOID"] = cancerRisk["FIPS"].astype(str) + cancerRisk["TRACT"]

	cancerRisk.to_csv('data/EPA_NATA/US_NATA05_NYgeoid.csv')
	return cancerRisk 

read_cancerRisk_CensusTract()