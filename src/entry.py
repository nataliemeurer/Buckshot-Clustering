import utils as util
import numpy as np

class entry:
	# Constructor: copy values over
	def __init__(self, values):
		self.values = values.copy();

	# get values
	def getValues():
		return self.values

	# calculateEuclidian Distance
	def euclidianDist(self, entry2):
		sumOfSquares = 0
		# For each key, we add to the sum of squares
		for key in self.values:
			# If it's a continuous variable, we calculate distance normally
			if util.isNumber(self.values[key]):
				# calculate the square of the values
				sumOfSquares += np.power(self.values[key] - entry2.getValues()[key], 2)
			else:
				if self.values[key] == entry.getValues()[key]:
					sumOfSquares += 0
				else:
					sumOfSquares += 1
		# Return the square root of the sum of squares
		return np.sqrt(sumOfSquares)
