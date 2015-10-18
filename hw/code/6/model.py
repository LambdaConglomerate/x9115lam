from random import *

class Model(object):

	def __init__(self, x):
		self.numOfVars = x
		self.constraints = []	#list of constraints
		self.constraintsTrack = {}	#dict mapping decision index to constraint index in self.constraints
		[self.constraintsTrack.update({i:[]}) for i in xrange(x + 1)]	#initialising constraint tracker
		self.bounds = {}	#dict of bounds in the form of {index:[min, max]}
		self.objectives = []	#list of objectives

	def addConstraint(self, indices, f):		#adds constraints
		constraintLocation = len(self.constraints)
		self.constraints.append(f)
		[self.constraintsTrack[i].append(constraintLocation) for i in indices]
		return self

	def addBound(self, indices, min, max): 	#adds bounds
		[self.bounds.update({x: [min,max]}) for x in indices]
		return self

	def addObjective(self, f):	#adds objective 
		self.objectives.append(f)
		return self

	def boundy(self, index):	# generates new single random decision within bounds
		return (self.bounds[index][1] - self.bounds[index][0]) * random() + self.bounds[index][0]

	def retry(self, *args):	#generates new random vector
		vector = self.transpose([self.boundy(x) for x in range(1, self.numOfVars + 1)])
		for i in range(1, self.numOfVars + 1):
			vector = self.singleRetry(vector, i)
		return vector

	def singleRetry(self, vector, index): #generates single random value for single index in decision within contraints
		vectorConstraints = self.constraintsTrack[index]	#side effect can change other indices (result of issues with Osyzka2)
		if(len(vectorConstraints) > 0):
			while(not reduce(lambda a,b: a & b, [self.constraints[i](vector) for i in vectorConstraints])):
				for i in range(1, self.numOfVars):
					if(len([x for x in self.constraintsTrack[i] if x in vectorConstraints]) > 0):
						vector[i] = self.boundy(i)
		return vector

	def transpose(self, vector): #transposes vector so first index is 1 instead of 0
		temp = range(1)
		temp.extend(vector)
		return temp

	def wrap(self, vector):	#wrap all values in vector
		return self.transpose([(vector[i] % (self.bounds[i][1] - self.bounds[i][0])) + self.bounds[i][0] for i in range(1, len(vector))])
	
	def initializeObjectiveMaxMin(self, vector):
		self.objectiveMaxs = [f(vector) for f in self.objectives]	#instantiate the max tracker for objectives
		self.objectiveMins = [f(vector) for f in self.objectives]	#instantiate the min tracker for objective

	def updateObjectiveMaxMin(self, vector):
		values = [f(vector) for f in self.objectives]
		changed = False
		for i in range(0, len(self.objectives)):
			if(values[i] > self.objectiveMaxs[i]):
				self.objectiveMaxs[i] = values[i]
				changed = True
			if(values[i] < self.objectiveMins[i]):
				self.objectiveMins[i] = values[i]
				changed = True
		if(changed):						#if objective bounds changed 
			return True						#return true so optimizer knows to update current energies
		else:
			return False

	def checkConstraints(self, vector): 
		if(len(self.constraints) > 0):
			return reduce(lambda a, b: True & a & b, [f(vector) for f in self.constraints])
		else:
			return True


	def energy(self,v):
		return((reduce(lambda a,b: a + b, [((f(v) - miny)/(maxy - miny))**2 for f, maxy, miny in zip(self.objectives, self.objectiveMaxs, self.objectiveMins)]))**(1/2.0) / ((len(self.objectives))**(1/2.0)))

