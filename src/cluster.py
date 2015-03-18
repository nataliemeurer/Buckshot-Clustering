import utils as util

class Cluster:
	# Constructor: takes an entry as the centroid and an array of entries as the second argument
	def __init__(self, centroid, points):
		self.centroid = centroid
		self.entries = points

	# get the current centroid
	def getCentroid():
		return self.centroid

	# get the entries
	def getEntries():
		return self.points

	def maxIntraClusterDistance(self):
		# declare a max distance of zero
		maxDistance = 0.0
		# for each entry
		util.updateProgress(0)
		for idx, entry in enumerate(self.entries):
			util.updateProgress(float(idx)/float(len(self.entries)))
			# don't compare entry to itself or entries that have already been compared
			for idx2, entry2 in enumerate(self.entries):
				if idx2 <= idx:
					continue
				else:
					distance = entry.euclidianDist(entry2)
					if distance > maxDistance:
						maxDistance = distance
		return maxDistance



