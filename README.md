# Analysis of Cancer Incidence Rates in New York State and Industrial Air Pollution
###### Steve Carrea, Andrew Fair

Cancer is one of the most common chronic diseases in New York State, and is second only to heart disease as the leading cause of death. Each year, about 100,000 New Yorkers are diagnosed with cancer. The effect of specific air pollutants on individual diseases and cancer is well documented. This project performs ordinary least squares linear regression on a specific set of chemicals: benzene, toluene, ethylbenzene, xylene (collectively referred to as BTEX compounds), formaldehyde, and dioxins. Benzene is a known carcinogen, especially for Leukemia, and the BTEX chemicals frequently co-occur at industrial facilities. Formaldehyde is a common toxin as it is released as a byproduct of incomplete combustion. Lastly, dioxins are the most toxic chemicals contained in our dataset and are emitted through a broad area of industries, including through combustion and processes such as paper manufacturing and pesticides. The lag time between exposure and development of cancer is taken into account. In the case of benzene, the highest risk of developing leukemia is incurred within the most recent 10 years of exposure. We use this lag time as a basis for choosing air emission data from the year 2000 and cancer data from the years 2005-2009.

*Note: this analysis does not take into traffic and other major contributors to air pollution, or air emissions reported outside the Toxic Release Inventory.*

## Cancer Data
Cancer incidence is the primary outcome of interest. By law, health providers must report every case of cancer to the NYS Dept of Health (DOH) through the NYS Cancer Registry. DOH makes these data available for 23 different types of cancer (plus an all-cancer total) for 2005-2009 at the census block-group level; we aggregated to the census tract and county levels for our investigation. A total of 3,826 census tracts reported cancer incidence rates.

## Smoking Data
Smoking is a risk factor for cancers of the lung, mouth, larynx, bladder, kidney, and several other organs. But having a risk factor, or even several, does not mean that you will get the disease. We use data that estimates the number of smokers in each area to control for smoking. The table below indicates whether smoking is the highest risk factor for each cancer type.

County-level smoking data were obtained from the 2008-2009 Expanded Behavioral Risk Factor Surveillance System (and from the 2009 Community Health Survey for NYC, specifically). The data represent percentage of cigarette smoking among adults for each county in NYS.  In lieu of census tract level smoking rates, we applied the county-level smoking rates to each census tract within the county. We did find that this reduced the resulting Pearson’s correlation between total cancer incidence and smoking from roughly 0.6 at the county level to 0.25 at the census tract level. *Note: a better downscaling method can be applied here.*

## Other confounders used
We use American Community Survey 2005-2009 five-year estimate data for the following variables, at both the county- and census tract-level: total population, age distribution, median household income, education level, and unemployment. We creat a categorical “percent elderly” variable from the age data by bifurcating at >= 65 years of age, and created a “higher education” categorical variable by splitting education at the level of some college or more. Total population was used not as a covariate but to normalize cancer incidence, which are reported as raw counts rather than rates.  

## Implementation
readFIPS.py: script to ensure that proper Census Tract codes are attached to each record in the table. In this case, the air emissions data was supplied with latitude and longitude coordinates for each facility. We used the FCC API  to return the U.S. Census Bureau Census Block number (i.e. the 15 character FIPS Code) given the passed latitude and longitude for each facility. 

airEmissions.py: script for processing and cleaning.

main.py file: to incorporate within the model and perform the linear regression perform using the ordinary least squares (OLS) method as provided by the statsmodel library found within the SciPy python package. We  find that our cross-sectional air emissions data is heteroscedastic and therefore we run our OLS model using heteroscedastic standard errors by calling the HC0 method within statsmodel. 

## Output

The program outputs a file for each model based upon the chemical into the regression folder. The script loops against the selected chemicals for all cancer types and writes all results to file in the regression folder, identifying those chemicals with coefficients greater than one and p-values less than 0.05. We review these results to find those we deem to be statistically significant. 

See correlation table to investigate the Pearson correlation between all imported variables at the same time.

## Result
Potential correlation between fugitive emissions of dioxin and esophagus, kidney, and pancreatic cancer. Also, between stack dioxins and kidney cancer. *Note for stack dioxins, there was only one reporting census tract at the time.*

## Cancers analyzed and risk factors:
The below information was taken from the American Cancer Society and other literature.

| Cancer Type  | Smoking | Industrial Chemicals | Industries |
|---|---|---|---|
| Bladder  | Highest | o-Toluidine, analine, benzidine, beta-naphthylamine | rubber, leather, textiles, paint products, printing |
| Bone  |   |
| Brain  |   | vinyl chloride | plastics |
| Breast  |   |
| Colorectal  |   |
| Esophagus  |   |
| Kidney  | High |
| Larynx  | High | wood dust, paint fumes  | metalworking, petroleum, plastics, textile
| Leukemia  |   | benzene | rubber, oil refining, gasoline-related industries, chemical manufacturing, shoe manufacturing |
| Liver  | | vinyl chloride |
| Lung  | High | arsenic, beryllium, cadmium, silica, vinyl chloride, nickel compounds, chromium compounds, coal products, mustard gas, chloromethyl ethers |
| Mesothelioma  |  |
| NHL  |   |
| Nasal  |   |
| Oral  |   |
| Other  |   |
| Ovary  |   |
| Pancreas  |   |   | metal refining
| Prostate  |   |
| Soft_Tissue  |   |
| Stomach  |   |
| Testis  |   |
| Thyroid  |   |
| Uterus  |   |

Notes:

* For brain cancer: exposure to vinyl chloride (a chemical used to manufacture plastics), petroleum products, and certain other chemicals have been linked with an increased risk of brain tumors in some studies but not in others.
* For leukemia: chemical exposure is more strongly linked to an increased risk of Acute Myeloid Leukemia (AML) than to other forms of leukemia.
