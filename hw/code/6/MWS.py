from Models import *
from random import *
import sys

def say(x):
 	sys.stdout.write(str(x)); sys.stdout.flush()




def MWS(model):
	max_changes = 1000
	max_retries = 100
	emin = 0
	s = model.retry()

	model.initializeObjectiveMaxMin(s)
	[model.updateObjectiveMaxMin(model.retry()) for i in range(100)] #prime the maxs and mins with values, avoids divide by 0

	e = model.energy(s)
	sb = list(s)
  	sbo = list(s)
  	eb = e
  	ebo = e
  	sn = list(sb)

  	for i in range(max_retries):
  		print '\nT:', i
  		for j in range(max_changes):
  			if e <= emin:
  				sbo = list(s)
  				ebo = e
  				break
  			c = randint(1, model.numOfVars)
  			if(random() >= 0.5):
  				sn = model.singleRetry(s, c)
  			else:
  				tempS = list(sn)
  				tempE = model.energy(sn)
  				for index in range(1, 10):
  					tempS[c] = (model.bounds[c][1] - model.bounds[c][0]) * (index/10.0)
  					if(model.checkConstraints(tempS)):
  						if(model.updateObjectiveMaxMin(tempS)):
  							e = model.energy(s)	#update all energies if new normal
  							eb = model.energy(sb)
  							ebo = model.energy(sbo)
  							en = model.energy(sn)
  							tempE = model.energy(tempS)
  						if(model.energy(tempS) < tempE):
  							sn = list(tempS)
  							tempE = model.energy(tempS)
  			en = model.energy(sn)
  			if en < eb:
  				sb = list(sn)
  				eb = en
  				say("!")
		  	if en < e:
		  		say("+")
		  	else:
		  		say(".")
		   	s = list(sn)
		   	e = en
		    # Print our best for that try
		print '\nSB:', sb
		print 'EB:', eb
		    # First check if the sb for that set of changes was better
		    # Than any of our other retries
		if(eb < ebo):
			sbo = list(sb)
			ebo = eb
		# Then retry with a brand new set of values
		s = model.retry()
		e = model.energy(s)
		sn = list(s)
		en = e
		sb = list(sn)
		eb = en		
	
	sbo.pop(0)
	print '\nEBO:', ebo
  	print 'SBO:', sbo



