import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import utils as util
import cluster as c

# read our file and store the data
data = arff.readArff(ENV.DATA_SRC)
# create a processing bin to manipulate our data
fullData = processor.dataBin(data)
fullData.fillMissingValues()	# fill all missing values
fullData.normalizeContinuousVariables()
entries = fullData.getDataAsEntries()
cluster = c.Cluster(entries[10], entries)
# fullData.normalizeAttribute('age')
# fullData.normalizeAttribute('education-num:')
