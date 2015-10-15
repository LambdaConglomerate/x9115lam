import collections, model, base, MaxWalkSat

def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def normalize(b1, b2):
  def n(x):
    return (x - b1) / (b2 - b1)
  return n

def schaffer():
  def f1(*args):
    args = args[0]
    return args[0] * args[0]
    return f1
  def f2(*args):
    args = args[0]
    return (args[0] - 2)**2
  return (f1, f2)


payload = collections.namedtuple('payload', ['decs', 'objs', 'cons', 'bound', 'energy'])
objectives = collections.namedtuple('objs', ['f1', 'f2'])
objective = collections.namedtuple('obj', ['func', 'norm'])
decs = collections.namedtuple('decs', ['x1'])
constraint = collections.namedtuple('constraint', ['ids', 'state'])
cons = None

funcs = schaffer()
obj1 = objective(funcs[0], normalize(0, 10000000000))
obj2 = objective(funcs[1], normalize(0, 9999600004))
objs = objectives(obj1, obj2)

decs = decs(bounds(-10**(5),10**(5)))


payload = payload(decs, objs, cons, True, 'from_hell')

m = model.model(payload)

fin = MaxWalkSat.run(m)
