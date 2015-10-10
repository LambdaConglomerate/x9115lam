import collections, model, MaxWalkSat

def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def normalize(b1, b2):
  def n(x):
    return (x - b1) / (b2 - b1)
  return n

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
    # print 'f1 args ', args
    return -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
  def f2(*args):
    args = args[0]
    # print 'f2 args ', args
    return args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2
  return (f1, f2)

payload = collections.namedtuple('payload', ['decs', 'objs', 'cons', 'bound', 'energy'])
objectives = collections.namedtuple('objs', ['f1', 'f2'])
objective = collections.namedtuple('obj', ['func', 'norm'])
decs = collections.namedtuple('decs', ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'])
constraint = collections.namedtuple('constraint', ['ids', 'state'])
cons = collections.namedtuple('cons', ['c1', 'c2', 'c3'])

funcs = osyczka2()
obj1 = objective(funcs[0], normalize(-640.908072277, -0.423436047808))
obj2 = objective(funcs[1], normalize(25.4899157903, 176.005656027))
objs = objectives(obj1, obj2)

decs = decs(bounds(0,10), bounds(0,10), bounds(1,5), bounds(0,6), bounds(1,5), bounds(0,10))

funcs = constraints()
c1 = constraint(('x1','x2'), funcs[0])
c2 = constraint(('x3','x4'), funcs[1])
c3 = constraint(('x5','x6'), funcs[2])
cons = cons(c1, c2, c3)

payload = payload(decs, objs, cons, True, 'from_hell')

m = model.model(payload)

fin = MaxWalkSat.run(m)

# vector = m.gen_con()
# print vector
# vector = m.gen_con()
# print 'length of decs', len(m.decs)
# print (m.check_con(vector, 'x' + str(7)))
# eval_list = m.eval_objs(vector)
# print m.energy(vector)
# print getattr(m.decs, 'x1')