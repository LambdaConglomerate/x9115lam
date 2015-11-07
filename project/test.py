from Models import *
from sa import *
from mws import *
from pso import *
#from pso import *

# full model list
# Osyczka2, Fonseca, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6, Tanaka, Constr_Ex, Srinivas, Golinski, Viennet2, Viennet3, Viennet4, Water
for m in [Osyczka2]:
    for o in [pso]:
        #Absolutely do not pass integers for retries or changes
        o(m, 50.0, 500.0)
