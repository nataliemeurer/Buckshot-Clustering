import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import utils as util

# read our file and store the data
data = arff.readArff(ENV.DATA_SRC)
# create a processing bin to manipulate our data
fullData = processor.dataBin(data)
fullData.fillMissingValues()	# fill all missing values
fullData.normalizeContinuousVariables()
# fullData.normalizeAttribute('age')
# fullData.normalizeAttribute('education-num:')
