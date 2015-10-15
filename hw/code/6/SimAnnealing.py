import random, math, sys

def neighbor(x, temp):
  epsilon = temp * random.random()
  add = bool(random.getrandbits(1))
  if add:
    x += epsilon
  else:
    x -= epsilon

  # Clipping
  if x < 0.0:
    x = x + 1.0
  if x > 1.0:
    x = x - 1.0

  return x

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

def prob(old, new, k):
  x = math.exp(((new - old) / k))
  return x

def sim_anneal(m):
  kmax = 10000.0
  emax = (2)**0.5

  # Not sure why we start with 1/2, but whatever
  s0 = 0.5
  s = s0
  e = m.energy(s)

  print "Initial energy", e
  sb = s
  eb = e
  k = 1.0

  say('(K:' + str(k) + ", SB:({0:.3f}) ".format(sb) + '\t')

  while k < kmax and e < emax:
    sn = neighbor(s, (kmax - k)/kmax)
    en = m.energy(sn)

    # Is this a best overall?
    if en > eb:
      sb = sn
      eb = en
      say("!")

    # Is this better than where we were last?
    if en > e:
      s = sn
      e = en
      say("+")

    elif prob(e, en, k / kmax) < random.random():
      s = sn
      e = en
      say("?")

    say(".")
    k += 1.00

    if k % 50 == 0:
      say("\n" + '(K:' + str(k) + ", SB:({0:.3f}) ".format(sb) + '\t')

  print '\n \nbest solution ' + str(sb)
  print 'energy of best solution ' + str(m.energy(sb))
