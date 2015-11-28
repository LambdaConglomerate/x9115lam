import math

c1 = [-273.3632, 75.2432]
c2 = [-273.048, 74.848]
n = min(len(c1), len(c2))
losses_a = [math.exp((a - b)/n) for (a,b) in zip(c1, c2)]
losses_a = sum(losses_a) / n
losses_b = [math.exp((a - b)/n) for (a,b) in zip(c2, c1)]
losses_b = sum(losses_b) / n
print "a: ", losses_a
print "b: ", losses_b

