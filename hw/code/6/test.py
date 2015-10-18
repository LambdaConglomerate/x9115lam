from Models import *
from SA import *
from MWS import *

for m in [Schaffer, Osyczka2, Kursawe]:
	for o in [SA, MWS]:
		o(m)
