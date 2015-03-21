import cluster as c
import entry as e
import numpy as np
import utils as util
import settings as ENV

# Main clustering class
class BuckshotClusters:
	# Constructor
	def __init__(self):
		self.resultsLog = []

	# Main clustering function
	def clusterEntries(self, entries):
		# STEP 1: Randomly select sqrt(n) adults and let them serve as our initial cluster centroids
		n = float(len(entries))			# store number of entries
		sqrtN = np.floor(np.sqrt(n))	# find the square root of our total number of entries
		clusters = []					# create a list to store our clusters
		iterator = 0					# create an iterator to manage while loop
		while iterator < sqrtN:
			iterator += 1
			entry = util.chooseOneWithoutReplacement(entries)
			clusters.append( c.Cluster(entry) )
		# STEP 2: Merge our initial clusters into K clusters using a matrix of values.  The centroid is recomputed each time they merge
		while len(clusters) > ENV.K:
			matrix = self.createGainMatrix(clusters)
			clusterIndices = getMaxCoords(matrix)

		# 2.These clusters are then merged into K clusters. One at a time, finding the best, or 
		# closest merge (single link). The centroids are then recomputed when merged. 
		
		# 3.Once there are K clusters, I add all N docs to the clusters. 
		
		# 4.If EXTENDED_K_MEANS_ALG is set to true: 
		# 1.the centroids are first recomputed, then the adults are re-assigned to the closest clusters. 
		
		# 2.The SSE is computed, and if it decreases the SSE larger than <MIN_ACCEPTABLE_SEE_DIMINISHING_PERCENT> of the previous, then it performs another round of K-means. 
		
		# 3.Finally, a graph is computed showing the SSE over each round 