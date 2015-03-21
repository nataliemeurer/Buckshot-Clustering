#  STORES ACCESSORY CLASSES AND FUNCTIONS
import bisect
import time, sys
import numpy as np
import math
import random
import settings as ENV

def scaleMinMax(value, oldMin, oldMax, minimum=0, maximum=1):
	return ((value - oldMin)/(oldMax - oldMin))*(maximum - minimum) + minimum

def scaleZScore(value, mean, stdev):
	return (value - mean) / stdev

def chooseOneWithoutReplacement(list):
	randIdx = math.floor(len(list) * random.random())
	removedVal = list.pop(int(randIdx))
	return removedVal

def chooseOneWithReplacement(list):
	randIdx = math.floor(len(list) * random.random())
	val = list[int(randIdx):int(randIdx) + 1]
	return val

# Merges Two dictionaries that use integers as values
def mergeDicts(dict1, dict2):
	newDict = {}
	for key in dict1:
		if key in dict2:
			newDict[key] = dict1[key] + dict2[key]
		else:
			newDict[key] = dict1[key]
	for key in dict2:
		if key in newDict:
			continue
		else:
			newDict[key] = dict2[key]
	return newDict


# Class used to manage sorted sets of a continuous variable
class continuousBin:
	def __init__(self, attrName):
		self.values = []
		self.attrName = attrName
		self.mean = None
		self.classMean = {}
		self.max = None
		self.min = None

	def add(self, val, className=ENV.CLASSIFIER_NAME):
		if val == "?":
			return
		if self.mean != None and isNumber(val):	
			self.mean = (float(self.mean) * float(len(self.values)) + val) / (float(len(self.values)) + 1)
			if className in self.classMean:
				self.classMean[className][0] = ((self.classMean[className][0] * self.classMean[className][1]) + val) / (self.classMean[className][1] + 1)
				self.classMean[className][1] += 1
			else:
				self.classMean[className] = [ val, 1 ]
			if val < self.min:
				self.min = val
			if val > self.max:
				self.max = val
			bisect.insort(self.values, val)
		else:
			self.mean = val
			self.min = val
			self.max = val
			self.classMean[className] = [ val, 1 ]
			self.values.append(val)

	def getValues(self):
		return self.values

	def getMean(self):
		return self.mean

	def getMin(self):
		return self.min

	def getMax(self):
		return self.max

	def getClassMean(self, className):
		if className in self.classMean:
			return self.classMean[className][0]
		else:
			return None

	def getAttrName(self):
		return self.attrName

# Class used to manage sets of a categorical variable
class categoricalBin:
	def __init__(self, types):
		self.categories = {}
		for type in types:
			self.categories[type] = 0
		self.categories['?'] = 0
		self.mode = None			# used to store overall mode of the bin
		self.classModes = {}		# used to store modes related to each class
		self.classCategories = {}	# used to store categories for each class

	# Adds one value to the bin
	def add(self, val, className):
		if self.mode != None:						# if we already have a mode
			self.categories[val] += 1 				# we add one to the categories count
			if self.categories[val] > self.mode[0]:	# if it's greater than the existing mode, we change the mode
				self.mode = [self.categories[val], val]
			classKey = str(val) + " " + className
			if classKey in self.classCategories:	# if the class name and value is in our categories
				self.classCategories[classKey] += 1
				if className in self.classModes:	# if the class name is  in our modes
					if self.classCategories[classKey] > self.classModes[className][0]:
						self.classModes[className] = [ self.classCategories[classKey], val ]
				else:
					self.classModes[className] = [ 1, val ]
			else:
				self.classCategories[classKey] = 1
		else:
			self.classModes[className] = [1, val]
			self.mode = [1, val]
			self.categories[val] += 1
			self.classCategories[str(val) + " " + className] = 1

	def getMode(self):
		return self.mode[1]

	def getClassMode(self, className):
		return self.classModes[str(className)][1]


# Returns whether the string can be converted to a number
def isNumber(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# Progress bar function -- Some functions inspired by this: http://stackoverflow.com/questions/3160699/python-progress-bar
def updateProgress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Pausing...\r\n"
    if progress >= 1:
        progress = 1
        status = "Processing complete..."
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
