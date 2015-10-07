import random, math, sys

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

def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

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

def osyczka2(x):
  f1 = -(25*(x[0]-2)**2 + (x[1] - 2)**2 + (x[2] - 1)**2 * (x[3]-4)**2 + (x[4] - 1)**2)
  f2 = x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2 + x[5]**2
  return (f1, f2)

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

  print 'f1 max ' +  str(f1_obs[-1][0])
  print 'f1 min ' + str(f1_obs[0][0])
  print 'f2 max ' + str(f2_obs[-1][1])
  print 'f2 min ' + str(f2_obs[0][1])

  # Returns normalization function for f1
  # norm_f1 = normalize(f1_obs[0][0], f1_obs[-1][0])

  # # Returns normalization function for f2
  # norm_f2 = normalize(f2_obs[0][1], f2_obs[-1][1])

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

base_runner()
base_runner()
base_runner()
base_runner()
