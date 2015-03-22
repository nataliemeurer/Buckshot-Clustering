# USED TO STORE GLOBAL / ENVIRONMENTAL VARIABLES

# GENERAL SETTINGS
PROGRESS_BAR = True 					# set whether a progress bar is used to show output.  Should be turned off when writing to files


# DATA SETTINGS
DATA_SRC = './data/adult-big.arff'


# PREPROCESSOR SETTINGS
FILL_WITH_CLASS_MODE = True 			# BOOLEAN: Determines whether the program fills missing values with the class mode or the overall mode
CLASSIFIER_NAME = "class" 				# STRING: Name of presumed classifier
REMOVE_OUTLIERS = True 					# BOOLEAN: Determines whether any outliers will be removed
REMOVE_ALL_OUTLIERS = False  			# BOOLEAN: If set to true, removes outliers from all continuous variables
REMOVED_OUTLIERS = ['age']				# LIST(strings): If remove all outliers, set to false, the list of attributes that will be scanned for outliers
OUTLIER_ZSCORE_THRESHOLD = [-2.5, 2.5]	# LIST(float): Range in which the z-score must fall for it to not be considered an outlier
NORMALIZATION_METHOD = "min-max"		# STRING: normalization method--serves as default in the normalize attribute function. Possible values: "z-score", "min-max"
NORMALIZED_MIN = 0						# INT: minimum value used for min-max normalization
NORMALIZED_MAX = 1  					# INT: maximum value used for min-max normalization
REMOVED_ATTRS = ["fnlwgt:", "education-num:"]	# LIST(strings): name of the attributes to be removed


# CLUSTERING SETTINGS
K = 9									# INT: number of clusters desired
DISTANCE_MEASURE = "euclidian"			# STRING: formula used to measure distance, currently only supports euclidian
MERGING_CRITERIA = "single-link"		# MERGING_CRITERIA: single-link, complete-link, avg-link, centroid, wards
MAX_SIMILARITY_THRESHOLD = 10			# sets the maximum distance threshold to merge two clusters

# VALIDATOR SETTINGS
NUM_OF_FOLDS = 10