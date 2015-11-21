import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def hm(corr):
	sns.set(style="white")


	# Generate a mask for the upper triangle
	mask = np.zeros_like(corr, dtype=np.bool)
	mask[np.triu_indices_from(mask)] = True

	# Set up the matplotlib figure
	f, ax = plt.subplots(figsize=(11, 9))

	# Generate a custom diverging colormap
	cmap = sns.diverging_palette(220, 10, as_cmap=True)

	# Draw the heatmap with the mask and correct aspect ratio
	sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
	            square=True, xticklabels=False, yticklabels=False,
	            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

	plt.yticks(rotation=0) 
	plt.xticks(rotation=90)
	# plt.show()
	plt.savefig('data/CorrelationTable/corrHM.png', bbox_inches='tight')