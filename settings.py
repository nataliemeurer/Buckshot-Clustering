# USED TO STORE GLOBAL / ENVIRONMENTAL VARIABLES

# GENERAL SETTINGS
PROGRESS_BAR = True 					# set whether a progress bar is used to show output.  Should be turned off when writing to files


# DATA SETTINGS
DATA_SRC = './data/adult-big.arff'


# PREPROCESSOR SETTINGS
FILL_WITH_CLASS_MODE = True 			# Determines whether the program fills missing values with the class mode or the overall mode
CLASSIFIER_NAME = "class" 				# Name of presumed classifier
NORMALIZATION_METHOD = "min-max"		# normalization method--serves as default in the normalize attribute function. Possible values: "z-score", "min-max"
NORMALIZED_MIN = 0						# minimum value used for min-max normalization
NORMALIZED_MAX = 1  					# maximum value used for min-max normalization


# CLUSTERING SETTINGS
K = 5									# number of clusters desired
DISTANCE_MEASURE = "euclidian"			# formula used to measure distance, currently only supports euclidian
MERGING_CRITERIA = "single-link"		# single-link, complete-link, avg-link, centroid, wards
MAX_SIMILARITY_THRESHOLD = 10			# sets the maximum distance threshold to merge two clusters

# VALIDATOR SETTINGS
NUM_OF_FOLDS = 10