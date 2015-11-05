from Models import *
from sa import *
from mws import *
from pso import *

for m in [Osyczka2]:
    for o in [pso]:
        #Absolutely do not pass integers for retries or changes
        o(m, 50.0, 500.0)
