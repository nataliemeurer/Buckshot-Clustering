import cluster as c
import entry as e
import numpy as np
import utils as util

# Main clustering class
class buckshotClusters:
	# Constructor
	def __init__(self):
		self.resultsLog = []

	# Main clustering function
	def clusterData(self, entries):

