# USED TO STORE GLOBAL / ENVIRONMENTAL VARIABLES

# General Settings
PROGRESS_BAR = True 							# set whether a progress bar is used to show output.  Should be turned off when writing to files

# File src, relative to main
DATA_SRC = './data/adult-big.arff'

# Preprocessor Preferences
FILL_WITH_CLASS_MODE = True

# Naive Bayes Preferences
CLASSIFIER_NAME = "native-country:"

# normalization method--serves as default in the normalize attribute function. Possible values: "z-score", "min-max"
NORMALIZATION_METHOD = "z-score"
NORMALIZED_MIN = 0
NORMALIZED_MAX = 1

# Validator Preferences
NUM_OF_FOLDS = 10