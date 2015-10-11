import random

r = random.random
rseed = random.seed

class Some:

  def __init__(i, max=8):
    i.n, i.any, i.max = 0,[],max

  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x
    return i

s = Some()
print s
s += "1"
print s
