import utils as util
import numpy as np
import settings
import bisect
import Queue as qu
import entry as e

# dataBin class manages and preprocesses all of our data
class dataBin:
	# constructor takes a single object, which will contain the data, reverseLookup information, continuous and discrete bins, attributes, and the name of our relation
	def __init__(self, data):
		self.data = data['data'] 				# our primary data store / source of truth
		self.lookup = data['lookup']			# gives us constant time lookup to find the entries for any value -- i.e. { "age 47": [ 1, 5, 7, 9]}
		self.attributes = data['attributes']	# our attributes, stored in a list [[attr1name, [categories]], [attr2name, 'real']]
		self.continuousVariables = data['continuousVariables']
		self.categoricalVariables = data['categoricalVariables']
		self.relation = data['relation']
		self.classIdx = data['classIdx']
		self.dataLength = float(len(self.data))
	
	# return the primary data
	def getData(self):
		return self.data

	# fills missing values using the mean or mode of the class and normalizes continuous variables
	def fillMissingValues(self):
		print "Filling all missing values with mean(continuous) or mode(categorical)"
		# for each attribute
		for attr in self.attributes:
			if attr[0] + " ?" in self.lookup:	# If we have undefined variables
				if attr[1] == 'real':
					# Fill missing continuous values
					self.fillMissingContinuousValues(attr[0])
				else:
					self.fillMissingCategoricalValues(attr[0])
				print "Filled missing values for " + attr[0]

	# Remove the named attribute from our data set
	def removeAttribute(self, attrName):
		print "Removing all " + attrName + " attributes\n"
		# Remove from main data
		for entry in self.data:
			entry.pop(attrName)
		# Remove from reverse lookup
		lookupKeys = []
		for key in self.lookup:
			if attrName in key:
				lookupKeys.append(key)
		for item in lookupKeys:
			self.lookup.pop(item)
		# Remove from continuous variable
		contVarKeys = []
		for key in self.continuousVariables:
			if attrName in key:
				contVarKeys.append(key)
		for item in contVarKeys:
			self.continuousVariables.pop(item)
		# Remove from continuous variable
		catVarKeys = []
		for key in self.categoricalVariables:
			if attrName in key:
				catVarKeys.append(key)
		for item in catVarKeys:
			self.categoricalVariables.pop(item)
		# Remove from attributes
		for idx, value in enumerate(self.attributes):
			if value[0] == attrName:
				self.attributes.pop(idx)
		for idx, value in enumerate(self.attributes):
			if value[0] == settings.CLASSIFIER_NAME:
				self.classIdx = idx

	# removes all outliers from the data set, based on z-score variables
	def removeAllOutliers(self):
		for key in self.continuousVariables:
			self.removeAttrOutliers(key)

	# Remove outliers for one continuous variables.  Outliers are defined as having a score > 2.5 or < -2.5
	def removeAttrOutliers(self, attrName):
		if attrName in self.continuousVariables:
			print "\n\nRemoving outliers for " + attrName + " based on z-score."
			stdev = np.std(self.continuousVariables[attrName].getValues());
			# store the indices of the entries we want to remove
			entriesToRemove = []
			util.updateProgress(0)
			for idx, entry in enumerate(self.data):
				util.updateProgress(float(idx)/float(len(self.data)))
				# get the entry's z-score
				zScore = util.scaleZScore(entry[attrName], self.continuousVariables[attrName].getMean(), stdev)
				if zScore > 2.5 or zScore < -2.5:
					entriesToRemove.append(idx)
			iterator = len(entriesToRemove) - 1
			util.updateProgress(1)
			print "\n"
			util.updateProgress(0)
			while iterator > -1:
				util.updateProgress(1.0 / float(iterator + 1.0))
				removedEntry = self.data.pop(entriesToRemove[iterator])
				for key in removedEntry:
					if util.isNumber(removedEntry[key]):
						self.continuousVariables[key].removeValue(removedEntry[key], removedEntry[settings.CLASSIFIER_NAME])
					else:
						self.categoricalVariables[key].removeValue(removedEntry[key], removedEntry[settings.CLASSIFIER_NAME])
				iterator -= 1
			util.updateProgress(1)
			print "\nRemoved " + str(len(entriesToRemove)) + " entries."
		else:
			print "Invalid Attribute requested for removal of outliers"


	# Normalize variables
	def normalizeContinuousVariables(self, method=settings.NORMALIZATION_METHOD, minimum=settings.NORMALIZED_MIN, maximum=settings.NORMALIZED_MAX):
		for attr in self.attributes:
			if attr[1] == 'real':
				# Fill missing continuous values
				self.normalizeAttribute(attr[0], minimum, maximum, method)

	# normalizes the attribute
	def normalizeAttribute(self, attrName, minimum=0, maximum=1, method=settings.NORMALIZATION_METHOD):
		if attrName in self.continuousVariables:
			print "\n\nNormalizing values for " + attrName + " using the " + method + " method:"
			util.updateProgress(0)
			attrIdx = None
			oldMin = self.continuousVariables[attrName].getMin();
			oldMax = self.continuousVariables[attrName].getMax();
			if method == "z-score":
				stdev = np.std(self.continuousVariables[attrName].getValues());
			newBin = util.continuousBin(attrName)
			for idx, attr in self.attributes:
				if attr[0] == attrName:
					attrIdx = idx
			# for every value of that attribute...
			for idx, entry in enumerate(self.data):
				util.updateProgress(float(idx) / float(len(self.data)))
				# Recalculate min max on a scale for the minimum and maximum
				if method == "min-max":
					newVal = util.scaleMinMax(entry[attrName], oldMin, oldMax, minimum, maximum)
				elif method == "z-score":
					newVal = util.scaleZScore(entry[attrName], self.continuousVariables[attrName].getMean(), stdev)
				else:
					return None
				# Add the value to the new bin
				newBin.add(newVal, self.attributes[self.classIdx][0])
				# Add the value to the data
				self.data[idx][attrName] = newVal
				newKey = str(attrName) + " " + str(newVal)
				# Add the value to our reverse lookup
				if newKey in self.lookup:
					self.lookup[newKey].append(idx)
				else:
					self.lookup[newKey] = [idx]
			# overwrite our old continuous bin with our new continuous bin
			util.updateProgress(1)
			self.continuousVariables[attrName] = newBin
		else:
			print "Attribute " + attrName + " was not found"
			return None

	# fills missing values for a single categorical classifier
	def fillMissingCategoricalValues(self, attrName):
		if attrName in self.categoricalVariables:
			# get and store the mode of that attribute
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for entryID in self.lookup[attrName + " ?"]:
					# Depending on our settings, we will either use the class mode or the overall mode
					if settings.FILL_WITH_CLASS_MODE == True and attrName != settings.CLASSIFIER_NAME:
						mode = self.categoricalVariables[attrName].getClassMode(self.data[entryID][settings.CLASSIFIER_NAME])
					else:
						mode = self.categoricalVariables[attrName].getMode()
					# replace their question mark with the mode
					self.data[entryID][attrName] = mode
					# add to the mode in the categorical variables
					self.categoricalVariables[attrName].add(mode, self.data[entryID][settings.CLASSIFIER_NAME])
				# move indices into proper location ['attr modeName']
				for filledUserID in self.lookup[attrName + " ?"]:
					mode = self.categoricalVariables[attrName].getClassMode(self.data[filledUserID][settings.CLASSIFIER_NAME])
					self.lookup[attrName + " " + mode].append(filledUserID)
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	# fills missing values for a single continuous classifier
	def fillMissingContinuousValues(self, attrName):
		if attrName in self.continuousVariables:
			# get and store the mean of that attribute
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for itemId in self.lookup[attrName + " ?"]:
					mean = self.continuousVariables[attrName].getClassMean(self.data[itemId][settings.CLASSIFIER_NAME])
					# replace their question mark with the mean
					if self.data[itemId][attrName] == '?':
						self.data[itemId][attrName] = mean
					# add to the mean in the continuous variables
					self.continuousVariables[attrName].add(mean, self.data[itemId][settings.CLASSIFIER_NAME])
					# move indices into proper location ['attr modeName']
					if attrName + " " + str(mean) in self.lookup:
						self.lookup[attrName + " " + str(mean)].append(itemId)
					else:
						self.lookup[attrName + " " + str(mean)] = [itemId]
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	# Returns the data points as entry objects
	def getDataAsEntries(self):
		entries = []
		print "\n\nConverting Data to entries"
		util.updateProgress(0)
		# converting data to proper format
		for idx, item in enumerate(self.data):
			util.updateProgress(float(idx)/ float(len(self.data)))
			# make a new entry
			entry = e.Entry(item)
			# add the entry
			entries.append(entry)
		util.updateProgress(1)
		print "\n"
		return entries
