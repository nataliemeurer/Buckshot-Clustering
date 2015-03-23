# USED TO STORE GLOBAL / ENVIRONMENTAL VARIABLES

# GENERAL SETTINGS
PROGRESS_BAR = True 							# BOOLEAN: set whether a progress bar is used to show output.  Should be turned off when writing to files


# DATA SETTINGS
DATA_SRC = './data/adult-big.arff'				# STRING: The path to the data file


# PREPROCESSOR SETTINGS
FILL_WITH_CLASS_MODE = True 					# BOOLEAN: Determines whether the program fills missing values with the class mode or the overall mode
CLASSIFIER_NAME = "class" 						# STRING: Name of presumed classifier
REMOVE_OUTLIERS = True 							# BOOLEAN: Determines whether any outliers will be removed
REMOVE_ALL_OUTLIERS = True  					# BOOLEAN: If set to true, removes outliers from all continuous variables
REMOVED_OUTLIERS = ['age']						# LIST(strings): If remove all outliers, set to false, the list of attributes that will be scanned for outliers
OUTLIER_ZSCORE_THRESHOLD = [-2.5, 2.5]			# LIST(float): Range in which the z-score must fall for it to not be considered an outlier
NORMALIZATION_METHOD = "min-max"				# STRING: normalization method--serves as default in the normalize attribute function. Possible values: "z-score", "min-max"
NORMALIZED_MIN = 0								# INT: minimum value used for min-max normalization
NORMALIZED_MAX = 1  							# INT: maximum value used for min-max normalization
REMOVED_ATTRS = ["fnlwgt:", "education-num:"]	# LIST(strings): name of the attributes to be removed


# CLUSTERING SETTINGS
USE_RANDOM_SAMPLE = True 						# BOOLEAN: Determines whether the algorithm will sample the whole data set or a fixed size
SAMPLE_SIZE = 15000 							# INT: Sets the sample size that the algorithm will cluster, which is randomly sampled without replacement
SAMPLE_WITH_REPLACEMENT = False 				# BOOLEAN: If true, samples data with replacement.  Otherwise, does not replace
K = 3											# INT: number of clusters desired
DISTANCE_MEASURE = "euclidian"					# STRING: formula used to measure distance, currently only supports euclidian
MERGING_CRITERIA = "single-link"				# STRING: single-link, complete-link, centroid, wards
USE_INTRA_CLUSTER_SHORTCUT = True 				# BOOLEAN: sets whether shortcut used in intra-cluster distance calculations.  The shortcut calculates distance from centroid instead of from all other points, making it O(n)
MAX_SIMILARITY_THRESHOLD = 5.0					# FLOAT: sets the maximum distance threshold to merge two clusters

# VALIDATOR SETTINGS
NUM_OF_FOLDS = 10