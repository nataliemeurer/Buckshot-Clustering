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
		# while len(clusters) > ENV.K:
		matrix = self.createComparisonMatrix(clusters)



	def createSimilarityMatrix(self, clusters):
		print "\nConstructing Similarity Matrix for " + str(len(clusters)) + "clusters using the " + ENV.MERGING_CRITERIA + " merging criteria."
		# Create a matrix full of None values of size equal to the length of clusters
		matrix = []
		count1 = 0
		minSimilarityVal = None
		maxSimilarityVal = None
		# Initialize matrix with all none values
		while count1 < len(clusters):
			count2 = 0
			matrix.append([])
			while count2 < len(clusters):
				matrix[count1].append(None)
				count2 += 1
			count1 += 1
		# for every single row
		for rowIdx, row in enumerate(matrix):
			# for each column
			for colIdx, col in enumerate(matrix):
				# we leave the value as None if 
				if rowIdx == colIdx:
					continue
				else:
					if ENV.MERGING_CRITERIA == "single-link":
						distance = clusters[rowIdx].singleLinkDist(clusters[colIdx])
						if minSimilarityVal == None:
							minSimilarityVal = [distance, rowIdx, colIdx]
							maxSimilarityVal = [distance, rowIdx, colIdx]
						if distance < minSimilarityVal:
							minSimilarityVal[0] = distance
							minSimilarityVal[1] = rowIdx
							minSimilarityVal[2] = colIdx
						if distance > maxSimilarityVal:
							maxSimilarityVal[0] = distance
							maxSimilarityVal[1] = rowIdx
							maxSimilarityVal[2] = colIdx
						matrix[rowIdx][colIdx] = distance

		