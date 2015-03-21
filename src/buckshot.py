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
			clusters.append( c.Cluster(entry, [e.Entry( entry.getValues().copy() )] ) )
		clusters[0].printClusterData()
		clusters[1].printClusterData()
		newCluster = c.mergeClusters(clusters[0], clusters[1])
		newCluster.printClusterData()
		print newCluster.maxIntraClusterDistance()
		