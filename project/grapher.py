import matplotlib.pyplot as plt
from model import *

class grapher(object):

	def __init__(s, model, numOfCans):
		s.allCansX = {}
		s.allCansY = {}
		for i in xrange(numOfCans):
			s.allCansX.update({i: []})
			s.allCansY.update({i: []})

		s.model = model

	def addVector(s, v, i):
		x, y = v[0], v[1]
		s.allCansX[i].append(x)
		s.allCansY[i].append(y)

	def graph(s):
		for i in s.allCansX:
			plt.scatter(s.allCansX[i], s.allCansY[i])

		plt.show()
