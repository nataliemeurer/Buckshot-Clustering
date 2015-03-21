import utils as util

class Cluster:
	# Constructor: takes an entry as the centroid
	def __init__(self, centroid):
		self.centroid = centroid
		self.entries = [points]
		self.categoricalAttrCounts = {}
		centroidVals = centroid.getValues()
		for key in centroidVals:
			if util.isNumber(centroidVals[key]) == False:
				self.categoricalAttrCounts[str(key) + " " + centroidVals[key]] = 1

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

	def addEntry(self, entry):
		entryVals = entry.getValues() 		# get the values we're adding
		centroidVals = centroid.getValues()	# get the values of our centroid
		# for each key, we update the centroid
		for key in entryVals:
			if key in centroidVals:
				# take the average of added numbers
				if util.isNumber(centroidVals[key]): 	# CONTINUOUS VARIABLES
					oldMean = centroidVals[key]
					newMean = (oldMean * float(len(self.points)) + flaot(entryVals[key])) / (float(len(self.points)) + 1.0)
					centroid.updateValue(key, newMean)
				else:									# CATEGORICAL VARIABLES
					attrKey = str(key) + " " + str(entryVals[key])
					if attrKey in self.categoricalAttrCounts:
						self.categoricalAttrCounts(attrKey) += 1
					else:
						self.categoricalAttrCounts(attrKey) = 1
					# check to see if we have a new mode.  if we do, update it in our centroid
					if self.categoricalAttrCounts(attrKey) > self.categoricalAttrCounts(key + " " + centroidVals[key]):
						centroid.updateValue(key, entryVals[key])
			else:
				return None
		# Add the value to our entries list
		self.entries.append(entry)
