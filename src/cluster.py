import utils as util
import entry as e

class Cluster:
	# Constructor: takes an entry as the centroid
	def __init__(self, centroid, values, catCounts={}):
		self.centroid = centroid
		self.entries = values
		self.categoricalAttrCounts = catCounts
		if util.dictIsEmpty(self.categoricalAttrCounts):
			centroidVals = centroid.getValues()
			for entry in self.entries:
				for key in centroidVals:
					if util.isNumber(centroidVals[key]) == False:
						self.categoricalAttrCounts[str(key) + " " + centroidVals[key]] = 1
	
	# Prints data related to the currnet cluster
	def printClusterData(self):
		print "\nCluster with " + str(len(self.entries)) + " entries and the following centroid attributes:"
		cVals = self.centroid.getValues()
		for key in cVals:
			print "\t" + key + " " + str(cVals[key])

	# get the current centroid
	def getCentroid(self):
		return self.centroid

	# get the entries
	def getEntries(self):
		return self.entries

	# Get list of categorical counts
	def getCatCounts(self):
		return self.categoricalAttrCounts

	# compute the maximum intracluster distance
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

	def singleLinkDist(self, cluster2):
		minDist = None
		for idx, entry in enumerate(self.entries):
			# don't compare entry to itself or entries that have already been compared
			for idx2, entry2 in enumerate(cluster2.getEntries()):
				distance = entry.euclidianDist(entry2)
				if minDist == None:
					minDist = distance
				elif distance < minDist:
					minDist = distance
		return minDist

	# Add an entry to the cluster
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
def mergeClusters(cluster1, cluster2):
	# Declare variables to refer to everything
	c1Count     = float(len(cluster1.getEntries()))
	c2Count     = float(len(cluster2.getEntries()))
	c1Centroid  = cluster1.getCentroid().getValues()
	c2Centroid  = cluster2.getCentroid().getValues()
	c1catCounts = cluster1.getCatCounts()
	c2catCounts = cluster2.getCatCounts()
	# update categorical counts
	newCatCounts = util.mergeDicts(c1catCounts, c2catCounts)
	newCentroid = {}
	# for each key, we find the new centroid's values
	for key in c1Centroid:
		if util.isNumber(c1Centroid[key]):	# if we're dealing with a continuous variable here
			newCentroid[key] = float(c1Centroid[key] * c1Count + c2Centroid[key] * c2Count) / float(c1Count + c2Count)
		else:								# we're dealing with a categorical variable
			# save time if the modes are the same
			if c1Centroid[key] == c2Centroid[key]:
				newCentroid[key] = c1Centroid[key]
			else:
				# determine the mode
				maxCount = 0	# store a maxCount
				maxVal = ""
				for catKey in newCatCounts:
					if key in catKey:
						if newCatCounts[catKey] > maxCount:
							maxCount = newCatCounts[catKey]
							maxVal = catKey.split(" ")[1]
					else:
						continue
				newCentroid[key] = maxVal
	newCluster = Cluster(e.Entry(newCentroid), cluster1.getEntries() + cluster2.getEntries(), newCatCounts)
	return newCluster
