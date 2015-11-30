import math

c1 = [250.90619794930973, 141.88259339345035]
c2 = [14.144825715501085, 64.55868802601792]
n = min(len(c1), len(c2))
losses_a = [math.exp((a - b)/n) for (a,b) in zip(c1, c2)]
losses_a = sum(losses_a) / n
losses_b = [math.exp((a - b)/n) for (a,b) in zip(c2, c1)]
losses_b = sum(losses_b) / n
print "a: ", losses_a
print "b: ", losses_b

