import collections, model, base, random

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
objs = objectives(funcs[0], funcs[1])

decs = decs(bounds(-10**(5),10**(5)))

payload = payload(decs, objs, cons, False, 'from_hell')

m = model.model(payload)

b = base.base(m)
b.run()
