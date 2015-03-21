import utils as util
import entry as e

class Cluster:
	# Constructor: takes an entry as the centroid
	def __init__(self, centroid):
		self.centroid = centroid
		centroidVals = centroid.getValues()
		self.entries = [e.Entry(centroidVals.copy())]
		self.categoricalAttrCounts = {}
		for key in centroidVals:
			if util.isNumber(centroidVals[key]) == False:
				self.categoricalAttrCounts[str(key) + " " + centroidVals[key]] = 1

	# get the current centroid
	def getCentroid(self):
		return self.centroid

	# get the entries
	def getEntries(self):
		return self.entries

	def getCatCounts(self):
		return self.categoricalAttrCounts

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

	def addEntry(self, entry):
		entryVals = entry.getValues() 		# get the values we're adding
		centroidVals = centroid.getValues()	# get the values of our centroid
		# for each key, we update the centroid
		for key in entryVals:
			if key in centroidVals:
				# take the average of added numbers
				if util.isNumber(centroidVals[key]): 	# CONTINUOUS VARIABLES
					oldMean = centroidVals[key]
					newMean = (oldMean * float(len(self.points)) + float(entryVals[key])) / (float(len(self.points)) + 1.0)
					centroid.updateValue(key, newMean)
				else:									# CATEGORICAL VARIABLES
					attrKey = str(key) + " " + str(entryVals[key])
					if attrKey in self.categoricalAttrCounts:
						self.categoricalAttrCounts[attrKey] += 1
					else:
						self.categoricalAttrCounts[attrKey] = 1
					# check to see if we have a new mode.  if we do, update it in our centroid
					if self.categoricalAttrCounts[attrKey] > self.categoricalAttrCounts[key + " " + centroidVals[key]]:
						centroid.updateValue(key, entryVals[key])
			else:
				return None
		# Add the value to our entries list
		self.entries.append(entry)


# merges two clusters and returns the result of the merge. Does not delete or alter either cluster
def mergeClusters(self, cluster2):
	# merge our values
	c1Count = float(len(cluster1.getEntries()))
	c2Count = float(len(cluster2.getEntries()))
	c1Centroid = cluster1.getCentroid().getValues()
	c2Centroid = cluster2.getCentroid().getValues()
	c1catCounts = cluster1.getCatCounts()
	c2catCounts = cluster2.getCatCounts()
	# update categorical counts
	newCatCounts = util.mergeDicts(c1catCounts, c2catCounts)
	newCentroid 
	for key in c1Centroid:
