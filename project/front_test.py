import math

c1 = [1.036795, 0.0472225]
c2 = [1.030512, 0.056647]
n = min(len(c1), len(c2))
losses_a = [math.exp((a - b)/n) for (a,b) in zip(c1, c2)]
losses_a = sum(losses_a) / n
losses_b = [math.exp((a - b)/n) for (a,b) in zip(c2, c1)]
losses_b = sum(losses_b) / n
print "a: ", losses_a
print "b: ", losses_b

# if losses_a < losses_b:
#   return
# else:
#   return
