from Models import *
from sa import *
from mws import *

for m in [Schaffer, Osyczka2, Kursawe]:
    for o in [sa, mws]:
        #Absolutely do not pass integers for retries or changes
        o(m, 50.0, 500.0)
