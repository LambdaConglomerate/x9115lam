from Models import *
from sa import *
from mws import *
#from pso import *

for m in [Osyczka2, Fonseca, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6, Tanaka, Constr_Ex, Srinivas, Golinski, Viennet2, Viennet3, Viennet4, Water]:
    for o in [sa]:
        #Absolutely do not pass integers for retries or changes
        o(m, 50.0, 500.0)
