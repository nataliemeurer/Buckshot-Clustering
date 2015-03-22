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
for attrName in ENV.REMOVED_ATTRS:
	fullData.removeAttribute(attrName)
fullData.fillMissingValues()				# fill all missing values
fullData.normalizeContinuousVariables()		# Normalize all continuous variables using the method specified in settings
entries = fullData.getDataAsEntries()		# convert all data points to the structure of an entry, a class I defined

# CLUSTERING
clusterDriver = buck.BuckshotClusters()		# create a cluster driver to do our clustering
clusterDriver.clusterEntries(entries)		# pass our data into the cluster to be buckshot clustered	