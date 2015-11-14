import pandas as pd 
import numpy as np

tri_2013 = pd.read_csv('data/EPA_TRI/toxic-release-inventory.ny.2013.geoid.csv')
tri_2000 = pd.read_csv('data/EPA_TRI/enigma-us.gov.epa.toxic-release-inventory.ny.2000-200f0a5398ae786411f001444769cccf.csv')

tri_2013_trim = tri_2013[["tri_facility_id","geoid"]]
print tri_2013_trim.drop_duplicates()

# tri_2000["geoid"] = np.nan
# tri_2000 = pd.merge(tri_2000, tri_2013, how='left')
# tri_2000.to_csv('data/EPA_TRI/toxic-release-inventory.ny.2000.geoid.csv')

# print tri_2000['geoid']