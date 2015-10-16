#Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from random import *
import math
import sys

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

def SA(model):

	emax = 0
	kmax = 10000.0
	k = 1

	s = model.retry()
	sb = s
	
	objectiveMaxs = [f(s) for f in model.objectives]	#instantiate the max tracker for objectives
	objectiveMins = [f(s) for f in model.objectives]	#instantiate the min tracker for objective

	def energy(v):
		return((reduce(lambda a,b: a + b, [((f(v) - miny)/(maxy - miny))**2 for f, maxy, miny in zip(model.objectives, objectiveMaxs, objectiveMins)]))**(1/2.0) / ((len(model.objectives))**(1/2.0)))
		
	def updateMaxMin(vector):				#tracks min and max, alternative to base runner
		values = [f(vector) for f in model.objectives]
		changed = False
		for i in range(0, len(model.objectives)):
			if(values[i] > objectiveMaxs[i]):
				objectiveMaxs[i] = values[i]
				changed = True
			if(values[i] < objectiveMins[i]):
				objectiveMins[i] = values[i]
				changed = True
		if(changed):						#if objective bounds changed update energies
			e = energy(s)
			eb = energy(sb)

	[updateMaxMin(model.retry()) for i in range(100)] #prime the maxs and mins with second values, avoids divide by 0

	e = energy(s)
	eb = e

	def prob(old, new, t): return(math.exp(((old - new) / t)))
		
	def neighbor(vector, t):
		
		for i in range(1, len(vector)):
			epsilon = t * random()
			if bool(getrandbits(1)): 		#not sure if we should random on each value
				vector[i] += epsilon		#or the whole vector
			else:
				vector[i] -= epsilon

		vector = model.wrap(vector)			#wrap
		for i in range(1, len(vector)):		#check all constraints for each vector
			vector = model.singleRetry(vector, i)	#will change value if constraints aren't met
											#could implement this differently
		return(vector)

	say("\n" + '(K:' + str(k) + ", SB:({0:.3f}) ".format(eb) + '\t')
	while((k < kmax) & (e > emax)):
		sn = neighbor(s, (kmax - k)/kmax)
		updateMaxMin(sn)
		en = energy(sn)

		if(en < eb):
			say( "!")
			sb = sn
			eb = en

		if((en < e)):
			say("+")
			s = sn
			e = en

		if(prob(e, en, (kmax - k)/kmax) > random()):
			say("?")
			s = sn
			e = en

		say(".")
		k += 1.00
		if k % 50 == 0:
			say("\n" + '(K:' + str(k) + ", SB:({0:.3f}) ".format(eb) + '\t')
			
	sb.pop(0)
	print(sb)
	print(eb)



	


	
