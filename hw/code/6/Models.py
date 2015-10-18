from model import *
import math

Osyczka2 = (Model(6)
				.addBound([1,2], 0, 10)		#usage: list of decision indices, min, max
				.addBound([3,5], 1, 5)
				.addBound([4], 0, 6)
				.addBound([6], 0, 10)
				.addConstraint([1,2], lambda x: (x[1] + x[2] - 2) >= 0)	#usage: list of decision indices, function
				.addConstraint([1,2], lambda x: (6 - x[1] - x[2]) >= 0)
				.addConstraint([1,2], lambda x: (2 + x[1] - x[2]) >= 0)
				.addConstraint([1,2], lambda x: (2 - x[1] + 3 * x[2]) >= 0)
				.addConstraint([3,4], lambda x: (4 - (x[3] - 3)**2 - x[4]) >= 0)
				.addConstraint([5,6], lambda x: ((x[5] - 3)**3 + x[6] - 4) >= 0)
				.addObjective(lambda x: -(25 * (x[1] - 2)**2 + (x[2] - 2)**2) + (x[3] - 1)**2 * (x[4] - 4)**2 + (x[5] - 1)**2)
				.addObjective(lambda x: x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2 + x[5]**2 + x[6]**2)
			)

Schaffer = (Model(1)
				.addBound([1], -10**5, 10**5)
				.addObjective(lambda x: x[1]**2)
				.addObjective(lambda x: (x[1]-2)**2)
			)


Ka = 0.8	#exponent values in kursawe
Kb = 3
Kn = 3	#n values for kursawe, default to 3
Kursawe = (Model(Kn)
				.addBound(range(1,Kn+1), -5, 5)
				.addObjective(lambda x: reduce(lambda a, b: a + b, [(-10 * math.exp(-0.2 * (math.sqrt(x[i]**2 + x[i+1]**2)))) for i in range(1,len(x) - 1)]))
				.addObjective(lambda x: reduce(lambda a, b: a + b, [abs(x[i])**Ka + 5 * math.sin(x[i])**Kb for i in range(1, len(x))]))
			)