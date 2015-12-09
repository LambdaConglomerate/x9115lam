from Models import *
from adaptiveGlobalPSO import *
from classicalGlobalPSO import *
from classicalGlobalPSOV2 import *
from PSO import *
from PSOProbs import *
from PSOv2 import *
#from pso import *

# full model list
# Osyczka2, Fonseca, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6, Tanaka, Constr_Ex, Srinivas, Golinski, Viennet2, Viennet3, Viennet4, Water
Two_D_List = [Osyczka2, Fonseca, ZDT1, ZDT2, ZDT3, ZDT4, Tanaka, Srinivas]
Three_D_List = [DTLZ1, DTLZ2, DTLZ3, DTLZ4, DTLZ5, DTLZ6, DTLZ7, Viennet2, Viennet3]

num_retries = 30.0
num_changes = 500.0

for m in [DTLZ5, DTLZ6, DTLZ7, Viennet2, Viennet3]:
    for o in [PSOv2]:
        #Absolutely do not pass integers for retries or changes
        if(len(sys.argv) > 1):
          o(m, num_retries, num_changes, out=sys.argv[1])
        else:
          o(m, num_retries, num_changes)
