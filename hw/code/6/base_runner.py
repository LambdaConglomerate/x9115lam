import random, math, sys, model
def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def constraints():
  def f(*args):
    args = args[0]
    if(args[0] + args[1] - 2 < 0): return False
    if(6 - args[0] - args[1] < 0): return False
    if(2 - args[1] + args[0] < 0): return False
    if(4 - (args[2] - 3)**2 - args[3] < 0): return False
    if((args[4] - 3)**3 + args[5] - 4 < 0): return False
    return True
  return f

def osyczka2():
  def f(*args):
    f1 = -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
    f2 = args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2
    return (f1, f2)
  return f

payload = {
  "decs": {"x1":bounds(0,10), "x2":bounds(0,10), "x3":bounds(1,5), "x4":bounds(0,6), "x5":bounds(1,5), "x6":bounds(0,10)},
  "objs": osyczka2(),
  "constraints": constraints()
}

m = model.model(payload)
m.gen_vals()

# def base_runner():
#   f1_obs = []
#   f2_obs = []
#   obs = []

#   # Run the baseline model test 1000 times
#   for j in range(10000):
#     x = generateValidValues()
#     y_tup = osyczka2(x)

#     obs.append(y_tup)

#     # Sort by f1 values
#     f1_obs = sorted(obs, key=lambda ob: ob[0])
#     # Sort by f2 values
#     f2_obs = sorted(obs, key=lambda ob: ob[1])

#   print 'f1 max ' +  str(f1_obs[-1][0])
#   print 'f1 min ' + str(f1_obs[0][0])
#   print 'f2 max ' + str(f2_obs[-1][1])
#   print 'f2 min ' + str(f2_obs[0][1])
