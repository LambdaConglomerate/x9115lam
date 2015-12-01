from Models import *
from adaptiveGlobalPSO import *
from classicalGlobalPSO import *
from classicalGlobalPSOV2 import *
# from adaptiveGlobalPSOwithProbs import *
#from pso import *

# full model list
# Osyczka2, Fonseca, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6, Tanaka, Constr_Ex, Srinivas, Golinski, Viennet2, Viennet3, Viennet4, Water
# Tanaka, Viennet2, Viennet3, Viennet4, Constr_Ex

for m in [DTLZ4]:
    for o in [adaptiveGlobalPSO]:
        #Absolutely do not pass integers for retries or changes
        o(m, 1.0, 500.0)
