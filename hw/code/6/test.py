import collections, model

def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def constraints():
  def c1(*args):
    args = args[0]
    if(args[0] + args[1] - 2 < 0): return False
    if(6 - args[0] - args[1] < 0): return False
    if(2 - args[1] + args[0] < 0): return False
    return True
  def c2(*args):
    args = args[0]
    if(4 - (args[2] - 3)**2 - args[3] < 0): return False
    return True
  def c3(*args):
    args = args[0]
    if((args[4] - 3)**3 + args[5] - 4 < 0): return False
    return True
  return (c1,c2,c3)

def osyczka2():
  def f1(*args):
    args = args[0]
    return -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
    return f1
  def f2(*args):
    args = args[0]
    return args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2
  return (f1, f2)


payload = collections.namedtuple('payload', ['decs', 'objs', 'cons'])
objectives = collections.namedtuple('objs', ['f1', 'f2'])

decs = collections.namedtuple('decs', ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'])

constraint = collections.namedtuple('constraint', ['ids', 'state'])
cons = collections.namedtuple('cons', ['c1', 'c2', 'c3'])

funcs = osyczka2()
objs = objectives(funcs[0], funcs[1])

decs = decs(bounds(0,10), bounds(0,10), bounds(1,5), bounds(0,6), bounds(1,5), bounds(0,10))

funcs = constraints()
c1 = constraint(('x1','x2'), funcs[0])
c2 = constraint(('x3','x4'), funcs[1])
c3 = constraint(('x5','x6'), funcs[2])
cons = cons(c1, c2, c3)

payload = payload(decs, objs, cons)

m = model.model(payload)
# m.gen_clean()
# vector = m.gen_con()
# m.eval_objs(vector)


def base_runner():
  f1_obs = []
  f2_obs = []
  obs = []

  # Run the baseline model test 1000 times
  for j in range(100000):
    x = m.gen_con()
    y_list = m.eval_objs(x)

    obs.append(y_list)

    # Sort by f1 values
  f1_obs = sorted(obs, key=lambda ob: ob[0])
    # print f1_obs
    # Sort by f2 values
  f2_obs = sorted(obs, key=lambda ob: ob[1])
    # print f2_obs

  print 'f1 max ' +  str(f1_obs[-1][0])
  print 'f1 min ' + str(f1_obs[0][0])
  print 'f2 max ' + str(f2_obs[-1][1])
  print 'f2 min ' + str(f2_obs[0][1])

base_runner()
