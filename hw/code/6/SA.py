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

	emin = 0
	kmax = 10000.0
	k = 1

	s = model.retry()
	sb = s
	
	model.initializeObjectiveMaxMin(s)

	[model.updateObjectiveMaxMin(model.retry()) for i in range(100)] #prime the maxs and mins with second values, avoids divide by 0

	e = model.energy(s)
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
	while((k < kmax) & (e > emin)):
		sn = neighbor(s, (kmax - k)/kmax)
		
		if(model.updateObjectiveMaxMin(sn)):	#check if new objective bounds
			e = model.energy(s)						#adjust accordingly 
			eb = model.energy(sb)
		
		en = model.energy(sn)

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
			say("\n" + '(K:' + str(k) + ", EB:({0:.3f}) ".format(eb) + '\t')
			
	sb.pop(0)
	print(sb)
	print(eb)



	


	
