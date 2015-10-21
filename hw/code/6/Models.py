from model import *
import math

Osyczka2 = (Model(6)
            # usage: list of decision indices, min, max
            .addBound([0, 1], 0, 10)
            .addBound([2, 4], 1, 5)
            .addBound([3], 0, 6)
            .addBound([5], 0, 10)
            # usage: list of decision indices, function
            .addConstraint([0, 1], lambda x: (x[0] + x[1] - 2) >= 0)
            .addConstraint([0, 1], lambda x: (6 - x[0] - x[1]) >= 0)
            .addConstraint([0, 1], lambda x: (2 + x[0] - x[1]) >= 0)
            .addConstraint([0, 1], lambda x: (2 - x[0] + 3 * x[1]) >= 0)
            .addConstraint([2, 3], lambda x: (4 - (x[2] - 3)**2 - x[3]) >= 0)
            .addConstraint([4, 5], lambda x: ((x[4] - 3)**3 + x[5] - 4) >= 0)
            .addObjective(lambda x: -(25 * (x[0] - 2)**2 + (x[1] - 2)**2) + (x[2] - 1)**2 * (x[3] - 4)**2 + (x[4] - 1)**2)
            .addObjective(lambda x: x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2 + x[5]**2)
            .addName("Osyczka2")
            )

Schaffer = (Model(1)
            .addBound([0], -10**5, 10**5)
            .addObjective(lambda x: x[0]**2)
            .addObjective(lambda x: (x[0] - 2)**2)
            .addName("Schaffer")
            )


Ka = 0.8  # exponent values in kursawe
Kb = 3
Kn = 3  # n values for kursawe, default to 3
Kursawe = (Model(Kn)
           .addBound(range(0, Kn), -5, 5)
           .addObjective(lambda x: reduce(lambda a, b: a + b,
                                          [(-10 * math.exp(-0.2 * (math.sqrt(x[i]**2 + x[i + 1]**2))))
                                           for i in range(0, len(x) - 1)]))
           .addObjective(lambda x: reduce(lambda a, b: a + b,
                                          [abs(x[i])**Ka + 5 * math.sin(x[i])**Kb
                                           for i in range(0, len(x) - 1)]))
           .addName("Kursawe")
           )
