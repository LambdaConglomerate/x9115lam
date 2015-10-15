import collections, model, math, MaxWalkSat

# these are parameters used for a and b in the second objective
a_param = 1
b_param = 1

def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def normalize(b1, b2):
  def n(x):
    return (x - b1) / (b2 - b1)
  return n

def kursawe():
  def f1(*args):
    args = args[0]
    sum = 0
    sum += -10 * math.exp(-0.2*math.sqrt(args[0]**2 + args[1]**2))
    sum += -10 * math.exp(-0.2*math.sqrt(args[1]**2 + args[2]**2))
    return sum
    return f1
  def f2(*args):
    args = args[0]
    sum = 0
    sum += abs(args[0])**a_param + 5 * math.sin(args[0])**b_param
    sum += abs(args[1])**a_param + 5 * math.sin(args[1])**b_param
    sum += abs(args[2])**a_param + 5 * math.sin(args[2])**b_param
    return sum
  return (f1, f2)


payload = collections.namedtuple('payload', ['decs', 'objs', 'cons', 'bound', 'energy'])
objectives = collections.namedtuple('objs', ['f1', 'f2'])
objective = collections.namedtuple('obj', ['func', 'norm'])
decs = collections.namedtuple('decs', ['x1', 'x2', 'x3'])
constraint = collections.namedtuple('constraint', ['ids', 'state'])
cons = None

funcs = kursawe()
obj1 = objective(funcs[0], normalize(-19.8575351929, -4.98880272393))
obj2 = objective(funcs[1], normalize(-10.587243916, 29.4348271457))
objs = objectives(obj1, obj2)

decs = decs(bounds(-5,5), bounds(-5,5), bounds(-5,5))

payload = payload(decs, objs, cons, True, 'from_hell')

m = model.model(payload)

fin = MaxWalkSat.run(m)
