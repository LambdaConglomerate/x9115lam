import random, math, sys

emax = (2)**0.5

# Calculates f1 and f2 and then
# returns the values in a tuple
# f1,f2
def osyczka2(x):
  f1 = -(25*(x[0]-2)**2 + (x[1] - 2)**2 + (x[2] - 1)**2 * (x[3]-4)**2 + (x[4] - 1)**2)
  f2 = x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2 + x[5]**2
  return (f1, f2)

#osyczka2 constraints: checks all costraints, returns true is all constraints met
#new mutation should be done if this returns false
def constraints12(x1, x2):
  if(x1 + x2 - 2 < 0): return False
  if(6 - x1 - x2 < 0): return False
  if(2 - x2 + x1 < 0): return False
  return True

def constraints34(x3, x4):
  if(4 - (x3 - 3)**2 - x4 < 0): return False
  return True

def constraints56(x5, x6):
  if((x5 - 3)**3 + x6 - 4 < 0): return False
  return True

#constraint stack, makes dealing with the step function easier
constraintsStack = []
constraintsStack.append(constraints12)
constraintsStack.append(constraints34)
constraintsStack.append(constraints56)

#returns bounds function that takes a random and returns a value within in the bounds
def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

# This returns the normalization function
# for one of the two observation functions (f1, f2)
# b1 is the minimum, b2 is the maximum
def normalize(b1, b2):
  def n(x):
    return (x - b1) / (b2 - b1)
  return n

# This returns the energy function for x
# basically it takes the two normalization
# functions as parameters and then treats those
# normalization functions return values as the
# x and y values in the x,y plane.  F1 returns x,
# f2 returns y.  We know for schaffer that hell
# is at (1,1) in this graph.  We calculate distance
# to hell from our x,y point and return it as our
# energy value.  For this simplified environment
# emax is sqrt(2)
def energy(f1_norm, f2_norm):
  def e(x):
    s = osyczka2(x)
    x = f1_norm(s[0])
    y = f2_norm(s[1])
    # print '\n'
    # print 'x is ' + str(x)
    # print 'f1 is ' + str(s[0])
    # print 'f2 is ' + str(s[1])
    # print 'f1 normlized is ' + str(x)
    # print 'f2 normalized is ' + str(y)
    dist_from_hell = ((1 - x)**2 + (1 - y)**2)**0.5
    # print 'dist from hell ' + str(dist_from_hell)
    return dist_from_hell / (2**(0.5))
  return e

# bounds:
# 0 <= x1 <= 10
# 0 <= x2 <= 10
# 1 <= x3 <= 5
# 0 <= x4 <= 6
# 1 <= x5 <= 5
# 0 <= x6 <= 10

#bound list, makes dealing with steps easier
xbounds = []
xbounds.append(bounds(0, 10))
xbounds.append(bounds(0, 10))
xbounds.append(bounds(1, 5))
xbounds.append(bounds(0, 6))
xbounds.append(bounds(1, 5))
xbounds.append(bounds(0, 10))

def generateValidValues():

  xtemp = []

  for i in range(0, 6):
    xtemp.append(xbounds[i](random.random()))

  while(not constraints12(xtemp[0], xtemp[1])):
    xtemp[0] = xbounds[0](random.random())
    xtemp[1] = xbounds[1](random.random())

  while(not constraints34(xtemp[2], xtemp[3])):
    xtemp[2] = xbounds[2](random.random())
    xtemp[3] = xbounds[3](random.random())

  while(not constraints56(xtemp[4], xtemp[5])):
    xtemp[4] = xbounds[4](random.random())
    xtemp[5] = xbounds[5](random.random())

  # say("\nxtemp = ")
  # say(xtemp)

  return(xtemp)

#TODO: adapt for oszyzcka2 constraints
def base_runner():
  f1_obs = []
  f2_obs = []
  obs = []

  # Run the baseline model test 1000 times
  for j in range(10000):
    x = generateValidValues()
    y_tup = osyczka2(x)

    obs.append(y_tup)

    # Sort by f1 values
    f1_obs = sorted(obs, key=lambda ob: ob[0])
    # Sort by f2 values
    f2_obs = sorted(obs, key=lambda ob: ob[1])

  # print 'f1 max ' +  str(f1_obs[-1][0])
  # print 'f1 min ' + str(f1_obs[0][0])
  # print 'f2 max ' + str(f2_obs[-1][1])
  # print 'f2 min ' + str(f2_obs[0][1])

  # Returns normalization function for f1
  norm_f1 = normalize(f1_obs[0][0], f1_obs[-1][0])

  # Returns normalization function for f2
  norm_f2 = normalize(f2_obs[0][1], f2_obs[-1][1])

  # This is all just a sanity check.  To make sure that
  # everything works as expected.  Check it out if you want.
  #

  # norm_f1_obs = [norm_f1(f1) for f1,f2 in f1_obs]
  # norm_f2_obs = [norm_f2(f2) for f1,f2 in f2_obs]

  # for norm_ob in norm_f2_obs:
  #   print norm_ob

  # print '---------------------'
  # print 'f1_max ' + str(f1_obs[-1][0])
  # print 'f1_max normalized ' + str(norm_f1(f1_obs[-1][0]))
  # print 'f1_min ' + str(f1_obs[0][0])
  # print 'f1_min normalized ' + str(norm_f1(f1_obs[0][0]))
  # print '---------------------'
  # print 'f2_max ' + str(f2_obs[-1][1])
  # print 'f2_max normalized ' + str(norm_f2(f2_obs[-1][1]))
  # print 'f2_min ' + str(f2_obs[0][1])
  # print 'f2_min normalized ' + str(norm_f2(f2_obs[0][1]))

  return (norm_f1, norm_f2)

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

def prob(old, new, k):
  x = math.exp(((new - old) / k))
  return x

def getConstraintPair(c):
  if(c == 0 or c == 1):
    return (0,1)
  elif(c == 2 or c == 3):
    return (2,3)
  else:
    return (4,5)

# Mutate one variable across its
# entire range, determining whether
# it has the best possible energy
def mutate(c, sn, energy):
  tempS = list(sn)
  tempE = energy(sn)
  #for the each tenth go through bounds of x
  for i in range(1, 10):
    stepX = xbounds[c](i / 10.0)
    #mutate
    tempS[c] = stepX
    #check constraints and if energy we are at a better energy
    #the call that was here before was genius but painful to read
    f, l = getConstraintPair(c)
    if constraintsStack[f/2](tempS[f], tempS[l]) and energy(tempS) > tempE:
      sn = list(tempS)
      tempE = energy(tempS)
  return sn

def tweak(c, sn):
    sn[c] = xbounds[c](random.random())
    f, l = getConstraintPair(c)
    while not constraintsStack[f/2](sn[f], sn[l]):
      sn[c] = xbounds[c](random.random())
    return sn

def maxWalkSat(energy):
  max_changes = 1000
  max_retries = 1000
  emax = 1
  s = generateValidValues()
  e = energy(s)
  sb = s
  sbo = s
  eb = e
  ebo = e
  sn = sb
  for i in range(max_retries):
    print '\nT:', i
    for j in range(max_changes):
      # print 'S', s
      if e >= emax:
        return s,e
      #pick the x to mutate
      c = random.randint(0, 5)
      if(random.random() >= 0.5):
        sn = tweak(c, sn)
      else:
        sn = mutate(c, sn, energy)
      en = energy(sn)
      if en > eb:
        sb = sn
        eb = en
        say("!")
      if en > e:
        say("+")
      else:
        say(".")
      s = list(sn)
      e = en
    # Print our best for that try
    print '\nSB:', sb
    print 'EB:', eb
    # First check if the sb for that set of changes was better
    # Than any of our other retries
    if(eb > ebo):
      sbo = list(sb)
      ebo = eb
    # Then retry with a brand new set of values
    s = generateValidValues()
    e = energy(s)
    sn = list(s)
    en = e
    sb = sn
    eb = en
  # If we're here we've run through all of our tries
  return sbo, ebo

if __name__ == "__main__":
  # norm_tup = base_runner()
  f1_min = -585.571879426
  f1_max = -1.02145704618
  f2_min = 25.4899157903
  f2_max = 166.215983078
  norm_f1 = normalize(f1_min, f1_max)
  norm_f2 = normalize(f2_min, f2_max)
  e = energy(norm_f1, norm_f2)
  s,e = maxWalkSat(e)
  print '\nEBO:', e
  print 'SBO:', s
