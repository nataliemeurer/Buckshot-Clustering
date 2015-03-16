import utils as util
import numpy as np
import settings
import bisect
import Queue as qu

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
	
	# return the primary data
	def getData(self):
		return self.data

	# fills all missing values using the mean or mode of the class
	def fillAllMissingValues(self):
		print "Filling all missing values with mean(continuous) or mode(categorical)"
		# for each attribute
		for attr in self.attributes:
			if attr[0] + " ?" in self.lookup:	# If we have undefined variables
				if attr[1] == 'real':
					self.fillMissingContinuousValues(attr[0])
				else:
					self.fillMissingCategoricalValues(attr[0])
				print "Filled missing values for " + attr[0]

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