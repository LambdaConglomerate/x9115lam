from Models import *
from random import *

def say(x):
 	sys.stdout.write(str(x)); sys.stdout.flush()


def MWS(model):
	max_changes = 100
	max_retries = 100
	emin = 0
	s = model.retry()

	model.initiateObjectiveMinMax(s)
	[model.updateObjectiveMaxMin(model.retry()) for i in range(100)] #prime the maxs and mins with second values, avoids divide by 0

	e = energy(s)
	sb = list[s]
  	sbo = list[s]
  	eb = e
  	ebo = e
  	sn = list[sb]

  	for i in range(max_retries):
  		print '\nT:', i
  		for j in range(max_changes):
  			if e <= emin:
        		return s,e
        	c = random.randint(1, model.numOfVars + 1)
        	if(random.random() >= 0.5):
        		sn = model.singleRetry(s, c)
      		else:
      			#change to sn later
        		for i in range(1, 10):
					vector[index] = (model.bounds[i][1] - model.bounds[i][0]) * (i/10.0)
						if(model.checkConstraints(vector)):
							if(model.updateObjectiveMaxMin(vector))	
								e = energy(s)	#update all energies if new normal
								eb = energy(sb)
								ebo = energy(sbo)
							if(model.energy(vector) < e):
								s = list[vector]
								e = energy(s)

