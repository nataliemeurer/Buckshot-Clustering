import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import utils as util
import cluster as c
import buckshot as buck


# FILE READING
data = arff.readArff(ENV.DATA_SRC)			# read our file and store the data

# PREPROCESSING
fullData = processor.dataBin(data)			# create a processing bin to manipulate our data
fullData.fillMissingValues()				# fill all missing values
for attrName in ENV.REMOVED_ATTRS:
	fullData.removeAttribute(attrName)		# if specific attributes have been requested to be removed, we do so here
if ENV.REMOVE_OUTLIERS == True:
	if ENV.REMOVE_ALL_OUTLIERS == True:		# if we need to remove all outliers, we do so here
		fullData.removeAllOutliers()
	else:
		for attrName in ENV.REMOVED_OUTLIERS:
			fullData.removeAttrOutliers(attrName)	# remove specific outliers
fullData.normalizeContinuousVariables()		# Normalize all continuous variables using the method specified in settings
entries = fullData.getDataAsEntries()		# convert all data points to the structure of an entry, a class I defined

# CLUSTERING
clusterDriver = buck.BuckshotClusters()		# create a cluster driver to do our clustering
if ENV.USE_RANDOM_SAMPLE == True:			# select a random sample to use for the cluster
	sample = []
	count = 0
	while count < ENV.SAMPLE_SIZE:
		if ENV.SAMPLE_WITH_REPLACEMENT == True:
			sample.append(util.chooseOneWithReplacement(entries))
		else:
			sample.append(util.chooseOneWithoutReplacement(entries))
		count += 1
	clusterDriver.clusterEntries(sample)
else:
	clusterDriver.clusterEntries(entries)		# pass our data into the cluster to be buckshot clustered	