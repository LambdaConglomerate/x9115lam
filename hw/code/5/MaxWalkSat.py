import random, math, sys

# Calculates f1 and f2 and then
# returns the values in a tuple
# f1,f2
def osyczka2(x1, x2, x3, x4, x5, x6):
  f1 = -(25*(x1-2)**2 + (x2 - 2)**2 + (x3 - 1)**2 * (x4-4)**2 + (x5 - 1)**2)
  f2 = x1**2 + x2**2 + x3**2 + x4**2 + x5**2 + x6**2
  return (f1, f2)

#osyczka2 constraints: checks all costraints, returns true is all constraints met
#new mutation should be done if this returns false
def constraints(x1, x2, x3, x4, x5, x6):
  if(x1 + x2 - 2 < 0): return False
  if(6 - x1 - x2 < 0): return False
  if(2 - x2 + x1 < 0): return False
  if(4 - (x3 - 3)**2 - x4 < 0): return False
  if((x5 - 3)**3 + x6 - 4 < 0): return False

  return True


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
# emax is sqrt(2).

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

    return dist_from_hell
  return e


#TODO: adapt for oszyzcka2 constraints
def base_runner():
  f1_obs = []
  f2_obs = []
  obs = []

  # Run the baseline model test 1000 times
  # bounds:
  # x1 >= 0
  # x2 <= 10
  # x3 >= 1
  # x5 <= 5
  # 0 <= x4 <= 6
  # 0 <= x6 <= 10
  for j in range(1000):
    x = random.random()
    y_tup = oszyzcka2(x)

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

def neighbor(x, temp):
  epsilon = temp * random.random()
  add = bool(random.getrandbits(1))
  if add:
    x += epsilon
  else:
    x -= epsilon

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

global kmax
global emax
kmax = 10000.0
emax = (2)**0.5

def sim_anneal(energy):
  s0 = 0.5
  s = s0
  e = energy(s)
  print "Initial energy", e
  sb = s
  eb = e
  k = 1.0
  
  say('(K:' + str(k) + ", SB:({0:.3f}) ".format(sb) + '\t')

  while k < kmax and e < emax:
    sn = neighbor(s, (kmax - k)/kmax)
    en = energy(sn)

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
  print 'energy of best solution ' + str(energy(sb))

if __name__ == "__main__":
  norm_tup = base_runner()
  e = energy(norm_tup[0], norm_tup[1])
  sim_anneal(e)
