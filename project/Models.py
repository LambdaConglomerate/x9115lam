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

Fonseca = (Model(3)
           .addBound(range(0, 3), -4, 4)
           .addObjective(lambda x: 1 - math.exp(-reduce(lambda a, b: a + b,
                                                             [(v - (1 / (len(x)**(0.5))))**2 for v in x])))
           .addObjective(lambda x: 1 - math.exp(-reduce(lambda a, b: a + b,
                                                             [(v + (1 / len(x)**(0.5)))**2 for v in x])))
           .addName("Fonseca")
           )

# ZDT shared function for ZDT1, 2, and 3
g1 = (lambda x: 1 + (9.0 * reduce(lambda a, b: a + b,
                                [x[i] for i in range(1, len(x))])) / (len(x) - 1.0))
ZDT1 = (Model(30)
        .addBound(range(0, 30), 0, 1)
        .addObjective(lambda x: x[0])
        .addObjective(lambda x: g1(x) * (1.0 - (x[0] / g1(x))**(0.5)))
        .addName("ZDT1")
        )

ZDT2 = (Model(30)
        .addBound(range(0, 30), 0, 1)
        .addObjective(lambda x: x[0])
        .addObjective(lambda x: g1(x) * (1 - (x[0] / g1(x))**(0.5)))
        .addName("ZDT2")
        )

ZDT3 = (Model(30)
        .addBound(range(0, 30), 0, 1)
        .addObjective(lambda x: x[0])
        .addObjective(lambda x: g1(x) * (1 - (x[0] / g1(x))**(0.2) - (x[0] / g1(x)) * math.sin(10 * math.pi * x[0])))
        .addName("ZDT3")
        )


g4 = (lambda x: 1 + (10 * (len(x) - 1) + reduce(lambda a, b: a + b,
                                                [(x[i]**2 - 10 * math.cos(4 * math.pi * x[i])) for i in range(1, len(x))])))

ZDT4 = (Model(10)
        .addBound([0], 0, 1)
        .addBound(range(1, 10), -5, 5)
        .addObjective(lambda x: x[0])
        .addObjective(lambda x: g4(x) * (1 - (x[1] / g4(x)))**(2))
        .addName("ZDT4")
        )

f6 = (lambda x: 1 - math.exp(-4 * x[0]) * math.sin(6 * math.pi * x[0])**(6))
g6 = (lambda x: 1 + 9.0 * (reduce(lambda a, b: a + b,
                                [x[i] for i in range(1, len(x))]) / (len(x) - 1))**(0.25))

ZDT6 = (Model(10)
        .addBound(range(0, 10), 0, 1)
        .addObjective(lambda x: f6(x))
        .addObjective(lambda x: g6(x) + (1 - (f6(x) / g6(x))**(2)))
        .addName("ZDT6")
        )

Tanaka = (Model(2)
          .addBound(range(0, 2), -math.pi, math.pi)
          .addConstraint([0, 1], lambda x: -x[0]**2 - x[1]**2 + 1 + 0.1 * math.cos(16 * math.atan(x[0] / x[1])) <= 0)
          .addConstraint([0, 1], lambda x: (x[0] - 0.5)**2 + (x[1] - 0.5)**2 <= 0.5)
          .addObjective(lambda x: x[0])
          .addObjective(lambda x: x[1])
          .addName("Tanaka")
          )

Constr_Ex = (Model(2)
             .addBound([0], 0.1, 1.0)
             .addBound([1], 0, 5)
             .addConstraint([0, 1],lambda x: x[1] + 9 * x[0] >= 6)
             .addConstraint([0, 1],lambda x: -x[1] + 9 * x[0] >= 1)
             .addObjective(lambda x: x[0])
             .addObjective(lambda x: (1 + x[1]) / x[0])
             .addName("ConstrEx")
             )

Srinivas = (Model(2)
            .addBound([0, 1], -20, 20)
            .addConstraint([0, 1], lambda x: x[0]**2 + x[1]**2 <= 225)
            .addConstraint([0, 1], lambda x: x[0] - 3 * x[1] <= -10)
            .addObjective(lambda x: (x[0] - 2)**2 + (x[1] - 1)**2 + 2)
            .addObjective(lambda x: 9 * x[0] - (x[1] - 1)**2)
            .addName("Srinivas")
            )

f2 = (lambda x: (745.0 * x[3] / (x[1] * x[2]) +
                 1.69 * 10**7)**(0.5) / (0.1 * x[5]**3))

Golinski = (Model(7)  # g2 constraint seems to be exactly the same as g1 so only g1 was added
            .addBound([0], 2.6, 3.6)
            .addBound([1], 0.7, 0.8)
            .addBound([2], 17.0, 28.0)
            .addBound([3, 4], 7.3, 8.3)
            .addBound([5], 2.9, 3.9)
            .addBound([6], 5.0, 5.5)
            .addConstraint([0, 1, 2], lambda x: (1.0 / (x[0] * (x[1]**2) * x[2]) - (1.0 / 27.0)) <= 0)
            .addConstraint([1, 2, 3, 5], lambda x: ((x[3]**3) / (x[1] * x[2]**2 * x[5]**4)) - (1.0 / 1.93) <= 0)
            .addConstraint([1, 2, 4, 6], lambda x: ((x[4]**3) / (x[1] * x[2] * x[6]**4)) - (1.0 / 1.93) <= 0)
            .addConstraint([1, 2], lambda x: x[1] * x[2] - 40 <= 0)
            .addConstraint([0, 1], lambda x: x[0] / x[1] - 12 <= 0)
            .addConstraint([0, 1], lambda x: 5 - x[0] / x[1] <= 0)
            .addConstraint([3, 5], lambda x: 1.9 - x[3] + 1.5 * x[5] <= 0)
            .addConstraint([4, 6], lambda x: 1.9 - x[4] + 1.1 * x[6] <= 0)
            .addConstraint([1, 2, 3, 5], lambda x: f2(x) <= 1300)
            .addConstraint([1, 2, 4, 6], lambda x: ((745.0 * x[4] / x[1] * x[2]) + 1.575 * 10**8)**(0.5) / (0.1 * x[6]**3) <= 1100)
            .addObjective(lambda x: 0.7854 * x[0] * x[1]**2 * ((10 * x[2]**2) / 3 + 14.933 * x[2] - 43.0934) - 1.508 * x[0] * (x[5]**2 + x[6]**2) + 7.477 * (x[5]**3 + x[6]**3) + 0.7854 * (x[3] * x[5]**2 + x[4] * x[6]**2))
            .addObjective(lambda x: f2(x))
            .addName("Golinski")
            )

Viennet2 = (Model(2)
            .addBound([0, 1], -4.0, 4.0)
            .addObjective(lambda x: ((x[0] - 2)**2) / 2.0 + ((x[0] + 1)**2) / 13.0 + 3.0)
            .addObjective(lambda x: ((x[0] + x[1] - 3)**2) / 36.0 + ((-x[0] + x[1] + 2)**2) / 8.0 - 17)
            .addObjective(lambda x: ((x[0] + 2 * x[1] - 1)**2) / 175.0 + ((2 * x[1] + x[0])**2) / 17.0 - 13)
            .addName("Viennet2")
            )

Viennet3 = (Model(2)
            .addBound([0, 1], -3.0, 3.0)
            .addObjective(lambda x: 0.5 * x[0]**2 + x[1]**2 + math.sin(x[0]**2 + x[1]**2))
            .addObjective(lambda x: ((3 * x[0] - 2 * x[1] + 4)**2) / 8.0 + ((x[0] - x[1] + 1)**2) / 27.0 + 15)
            .addObjective(lambda x: 1 / (x[0]**2 + x[1]**2 + 1) - 1.1 * math.exp(-x[0]**2 - x[1]**2))
            .addName("Viennet3")
            )

Viennet4 = (Model(2)
            .addBound([0, 1], -4.0, 4.0)
            .addConstraint([0, 1], lambda x: -x[1] - 4 * x[0] + 4 >= 0)
            .addConstraint([0], lambda x: x[0] + 1 >= 0)
            .addConstraint([0, 1], lambda x: x[1] - x[0] + 2 >= 0)
            .addObjective(lambda x: ((x[0] - 2)**2) / 2.0 + ((x[1] + 1)**2) / 13.0 + 3)
            .addObjective(lambda x: ((x[0] + x[1] - 3)**2) / 175.0 + ((2 * x[1] - x[0])**2) / 17.0 - 13)
            .addObjective(lambda x: ((3 * x[0] - 2 * x[1] + 4)**2) / 8.0 + ((x[0] - x[1] + 1)**2) / 27.0 + 15)
            .addName("Viennet4")
            )

Water = (Model(3)
         .addBound([0], 0.01, 0.45)
         .addBound([1], 0.01, 0.10)
         .addBound([2], 0.01, 0.10)
         .addConstraint([0, 1], lambda x: 1 - 0.00139 / (x[0] * x[1]) + 4.94 * x[2] - 0.08 >= 0)
         .addConstraint([0, 1, 2], lambda x: 1 - 0.000306 / (x[0] * x[1]) + 1.082 * x[2] - 0.0986 >= 0)
         .addConstraint([0, 1, 2], lambda x: 5000 - 12.307 / (x[0] * x[1]) + 4.9408 * x[2] + 4051.02 >= 0)
         .addConstraint([0, 1, 2], lambda x: 16000 - 2.09 / (x[0] * x[1]) + 8046.33 * x[2] - 696.71 >= 0)
         .addConstraint([0, 1, 2], lambda x: 10000 - 2.138 / (x[0] * x[1]) + 7883.39 * x[2] - 705.04 >= 0)
         .addConstraint([0, 1, 2], lambda x: 2000 - 0.417 / (x[0] * x[1]) + 1721.26 * x[2] - 136.54 >= 0)
         .addConstraint([0, 1, 2], lambda x: 550 - 0.164 / (x[0] * x[1]) + 631.13 * x[2] - 54.48 >= 0)
         .addObjective(lambda x: 106780.37 * (x[1] * x[2]) + 61704.67)
         .addObjective(lambda x: 3000 * x[0])
         .addObjective(lambda x: 305700 * 2289 * x[1] / (0.06 * 2289)**0.65)
         .addObjective(lambda x: 250 * 2289 * x[1] * math.exp(-39.75 * x[1] + 9.9 * x[2] + 2.74))
         .addObjective(lambda x: 25 * 1.39 / (x[0] * x[1] + 4940 * x[2] - 80))
         .addName("Water")
         )

#############################################################
# START OF DTLZ1
#############################################################

# Number of objective dimensions
m_dtlz1 = 3
# 5 is recommended
k_dtlz1 = 5
# Number of decisions
n_dtlz1 = m_dtlz1 + k_dtlz1 - 1

# g function for DTLZ1
g_dtlz1 = lambda x: 100 * (n_dtlz1 + sum(\
    [(x[i] - 0.5)**2 - math.cos(20 * math.pi * (x[i] - 0.5)) for i in xrange(n_dtlz1)]))


DTLZ1 = (Model(n_dtlz1)
        .addName("DTLZ1")
        .addObjective(lambda x: 0.5 * x[0] * x[1] * (1 + g_dtlz1(x)))
        .addObjective(lambda x: 0.5 * x[0] * (1 - x[1]) * (1 + g_dtlz1(x)))
        .addObjective(lambda x: 0.5 * (1 - x[0]) * (1 + g_dtlz1(x)))
        )

for i_1 in xrange(n_dtlz1):
    DTLZ1.addBound([i_1], 0, 1)

#############################################################
# START OF DTLZ2
#############################################################

# Number of objective dimensions
m_dtlz2 = 3
# 10 is recommended
k_dtlz2 = 10
# Number of decisions
n_dtlz2 = m_dtlz2 + k_dtlz2 - 1

# g function for DTLZ2
g_dtlz2 = lambda x: sum(\
    [(x[i] - 0.5)**2 for i in xrange(n_dtlz2)])

DTLZ2 = (Model(n_dtlz2)
        .addName("DTLZ2")
        .addObjective(lambda x: (1 + g_dtlz2(x)) * math.cos(x[0]*math.pi/2.0) * math.cos(x[1]*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz2(x)) * math.cos(x[0]*math.pi/2.0) * math.sin(x[1]*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz2(x)) * math.sin(x[0]*math.pi/2.0))
        )

for i_2 in xrange(n_dtlz2):
    DTLZ2.addBound([i_2], 0, 1)

#############################################################
# START OF DTLZ3
#############################################################

# Number of objective dimensions
m_dtlz3 = 3
# 10 is recommended
k_dtlz3 = 10
# Number of decisions
n_dtlz3 = m_dtlz3 + k_dtlz3 - 1

# g function for DTLZ3 is same as for DTLZ1
g_dtlz3 = lambda x: 100 * (n_dtlz3 + sum(\
    [(x[i] - 0.5)**2 - math.cos(20 * math.pi * (x[i] - 0.5)) for i in xrange(n_dtlz3)]))

DTLZ3 = (Model(n_dtlz3)
        .addName("DTLZ3")
        .addObjective(lambda x: (1 + g_dtlz3(x)) * math.cos(x[0]*math.pi/2.0) * math.cos(x[1]*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz3(x)) * math.cos(x[0]*math.pi/2.0) * math.sin(x[1]*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz3(x)) * math.sin(x[0]*math.pi/2.0))
        )

for i_3 in xrange(n_dtlz3):
    DTLZ3.addBound([i_3], 0, 1)

#############################################################
# START OF DTLZ4
#############################################################

# Number of objective dimensions
m_dtlz4 = 3
# 10 is recommended
k_dtlz4 = 10
# Number of decisions
n_dtlz4 = m_dtlz4 + k_dtlz4 - 1
# 100 is recommended
dtlz4_alpha = 100
# g function for DTLZ4 (same as for DTLZ2)
g_dtlz4 = lambda x: sum(\
    [(x[i] - 0.5)**2 for i in xrange(n_dtlz4)])

DTLZ4 = (Model(n_dtlz4)
        .addName("DTLZ4")
        .addObjective(lambda x: (1 + g_dtlz4(x)) * math.cos((x[0]**dtlz4_alpha)*math.pi/2.0) * math.cos((x[1]**dtlz4_alpha)*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz4(x)) * math.cos((x[0]**dtlz4_alpha)*math.pi/2.0) * math.sin((x[1]**dtlz4_alpha)*math.pi/2.0))
        .addObjective(lambda x: (1 + g_dtlz4(x)) * math.sin((x[0]**dtlz4_alpha)*math.pi/2.0))
        )


for i_4 in xrange(n_dtlz4):
    DTLZ4.addBound([i_4], 0, 1)

#############################################################
# START OF DTLZ5
#############################################################

# Number of objective dimensions
m_dtlz5 = 3
# 10 is recommended
k_dtlz5 = 10
# Number of decisions
n_dtlz5 = m_dtlz5 + k_dtlz5 - 1

# g function for DTLZ5 (same as for DTLZ2)
g_dtlz5 = lambda x: sum(\
    [(x[i] - 0.5)**2 for i in xrange(n_dtlz5)])

#theta function for DTLZ5
theta_dtlz5 = lambda x, i: (math.pi)/(4*(1 + g_dtlz5(x)))*(1 + 2*g_dtlz5(x)*x[i])

DTLZ5 = (Model(n_dtlz5)
        .addName("DTLZ5")
        .addObjective(lambda x: (1 + g_dtlz5(x)) * math.cos(x[0]*math.pi/2.0) * math.cos(theta_dtlz5(x, 1)))
        .addObjective(lambda x: (1 + g_dtlz5(x)) * math.cos(x[0]*math.pi/2.0) * math.sin(theta_dtlz5(x, 1)))
        .addObjective(lambda x: (1 + g_dtlz5(x)) * math.sin(x[0]*math.pi/2.0))
        )

for i_5 in xrange(n_dtlz5):
    DTLZ5.addBound([i_5], 0, 1)

#############################################################
# START OF DTLZ6
#############################################################

# Number of objective dimensions
m_dtlz6 = 3
# 10 is recommended
k_dtlz6 = 10
# Number of decisions
n_dtlz6 = m_dtlz6 + k_dtlz6 - 1

# g function for DTLZ6
g_dtlz6 = lambda x: sum(\
    [(x[i])**0.1 for i in xrange(n_dtlz5)])

#theta function for DTLZ6 (same as for DTLZ5)
theta_dtlz6 = lambda x, i: (math.pi)/(4*(1 + g_dtlz6(x)))*(1 + 2*g_dtlz6(x)*x[i])

DTLZ6 = (Model(n_dtlz6)
        .addName("DTLZ6")
        .addObjective(lambda x: (1 + g_dtlz6(x)) * math.cos(x[0]*math.pi/2.0) * math.cos(theta_dtlz6(x, 1)))
        .addObjective(lambda x: (1 + g_dtlz6(x)) * math.cos(x[0]*math.pi/2.0) * math.sin(theta_dtlz6(x, 1)))
        .addObjective(lambda x: (1 + g_dtlz6(x)) * math.sin(x[0]*math.pi/2.0))
        )

for i_6 in xrange(n_dtlz6):
    DTLZ6.addBound([i_6], 0, 1)

#############################################################
# START OF DTLZ7
#############################################################

# Number of objective dimensions
m_dtlz7 = 3
# 20 is recommended
k_dtlz7 = 20
# Number of decisions
n_dtlz7 = m_dtlz7 + k_dtlz7 - 1

# g function for DTLZ7
g_dtlz7 = lambda x: 1 + (9)/(k_dtlz7) * sum(\
    [x[i] for i in xrange(n_dtlz7)])

#h function for DTLZ7
h_dtlz7 = lambda x, f1, f2: 3 - ((f1)/(1 + g_dtlz7(x)) * (1 + math.sin(3 * math.pi * f1))) + ((f2)/(1 + g_dtlz7(x)) * (1 + math.sin(3 * math.pi * f2)))

DTLZ7 = (Model(n_dtlz7)
        .addName("DTLZ7")
        .addObjective(lambda x: x[0])
        .addObjective(lambda x: x[1])
        .addObjective(lambda x: (1 + g_dtlz7(x)) * h_dtlz7(x, x[0], x[1]))
        )

for i_7 in xrange(n_dtlz7):
    DTLZ7.addBound([i_7], 0, 1)
