import random, math, sys, collections, mws
class model(object):
  def __init__(self, decs, cons, objs, norm_objs, wrap, name):
    self.payload = payload(decs, cons, objs, norm_objs, wrap, name)
    # print self.payload.decs

  def get_name(self):
    return self.payload.name

  def num_decs(self):
    return len(self.payload.decs)

  def gen_clean(self):
    return [self.gen_dec(dec) for dec in self.payload.decs]

  def gen_con(self, vect=None):
    # If we don't have any constraints
    # we don't need to do anything
    # other than regen a new vector
    if self.payload.cons == None:
      return self.gen_clean()
    # If we're calling for the first time
    # generate a blank vector
    if not vect:
      vect = self.gen_clean()
    # This is set up to try three things
    # each time there is a problem with a constraint
    # it first tries to generate either dec in
    # the constraint, then both.  If that fails
    # it loops back and tries again.
    for c in self.payload.cons:
      while not c.state(vect):
        # print('c is', c)
        t1 = self.gen_spec(vect, c.ids[0])
        t2 = self.gen_spec(vect, c.ids[1])
        t3 = self.gen_spec(vect, c.ids)
        if c.state(t1):
          vect = t1
        if c.state(t2):
          vect = t2
        if c.state(t3):
          vect = t3
    return vect

  def gen_spec(self, vect, ids):
    # We don't really need to deal with multiple ids
    # yet, since if we call with one id 0,1 or 2,3
    # we can just index based on the first id.
    if isinstance(ids, tuple):
      for id in ids:
        vect[id] = self.gen_dec(self.payload.decs[id])
    else:
      vect[ids] = self.gen_dec(self.payload.decs[ids])
    return vect

  def gen_dec(self, dec):
    min = dec[0]
    max = dec[1]
    return ((max-min) * random.random()) + min

  def get_min(self, id):
    return self.payload.decs[id][0]

  def get_max(self, id):
    return self.payload.decs[id][1]

  def add_epsilon(self, id, vect, epsilon):
    tmp = vect[id]
    vect[id] += epsilon
    vect[id] = self.payload.o_o_bounds(id, vect[id])
    if(self.check_con(vect, id)):
      return vect
    else:
      vect[id] = tmp
      return vect

  def eval_objs(self, vect):
    if self.payload.norm_objs:
      return [self.norm(obj.func(vect), obj) for obj in self.payload.objs]
    else:
      return [obj(vect) for obj in self.payload.objs]

  def norm(self, x, obj):
    min, max = obj.min_max
    x = (x - min) / (max - min)
    return x

  # This approach might really not work
  # forever.
  # Additionally this assumes that each decision
  # is only involved in one set of constraints.
  # If that isn't true we need to make changes here.
  def check_con(self, vector, id):
    if not self.payload.cons:
      # If we're in here there aren't constraints
      return True
    for c in self.payload.cons:
      for i in c.ids:
        if id == i:
          # print c
          return(c.state(vector))
    # This should never happen, but if it does
    # we will know something is wrong.
    return None

class payload(object):
  def __init__(self, decs, cons, objs, norm_objs, wrap, name):
    decs_tup = collections.namedtuple('decs', ['x' + str(x) for x in range(0, len(decs)) ])
    self.decs = decs_tup(*decs)
    if cons:
      con_tup = collections.namedtuple('constraint', ['ids', 'state'])
      cons_tup = collections.namedtuple('cons', ['c' + str(x) for x in range(0, len(cons))])
      self.cons = cons_tup(*[con_tup(*x) for x in cons])
    else:
      self.cons = None
    objs_tup = collections.namedtuple('objs', ['f' + str(x) for x in range(0, len(objs))])
    self.norm_objs = norm_objs
    if norm_objs:
      obj_tup = collections.namedtuple('obj', ['func', 'min_max'])
      self.objs = objs_tup(*[obj_tup(*x) for x in objs])
    else:
      obj_tup = collections.namedtuple('obj', ['func'])
      self.objs = objs_tup(*[obj_tup(*x) for x in objs])
    if wrap:
      self.o_o_bounds = self.wrap
    else:
      self.o_o_bounds = self.peg
    self.name = name

  def print_decs(self):
    print self.decs
    print '\n'

  def print_cons(self):
    print self.cons
    print '\n'

  def print_objs(self):
    print self.objs
    print '\n'

  # This funciton could just continue wrapping
  # until we reached a point that the wrapped value
  # was in bounds, but rather than go through that
  # over and over again it seemed easier to just wrap
  # once and then peg if we have to.
  def wrap(self, id, x):
    min = self.decs[id][0]
    max = self.decs[id][1]
    if x < min:
      mag = abs(abs(x) - abs(min))
      x = max - mag
      if x < min: return min
    elif x > max:
      mag = abs(abs(x) - abs(max))
      x = min + mag
      if x > max: return max
    return x

  def peg(self, id, x):
    min = self.decs[id][0]
    max = self.decs[id][1]
    if x < min:
      return min
    elif x > max:
      return max
    return x

# def c0(args):
#   if(args[0] + args[1] - 2 < 0): return False
#   if(6 - args[0] - args[1] < 0): return False
#   if(2 - args[1] + args[0] < 0): return False
#   return True
# def c1(args):
#   if(4 - (args[2] - 3)**2 - args[3] < 0): return False
#   return True
# def c2(args):
#   if((args[4] - 3)**3 + args[5] - 4 < 0): return False
#   return True

# def f0(args):
#   return -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
# def f1(args):
#   return args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2

# decs_list = (0,10), (0,10), (1,5), (0,6), (1,5), (0,10)
# constraint_list = ((0,1),c0), ((2,3),c1), ((4,5),c2)
# obs_list = (f0, (-640.908072277, -0.423436047808)), (f1, (25.4899157903, 176.005656027))

# m = model(decs_list, constraint_list, obs_list, True, True)
# v1 = m.gen_con()
# print(v1)
# v2 = m.gen_spec(v1, 0)
# m.add_epsilon(0, v2, -8)
# print(v2)
# m.add_epsilon(0, v2, 8)
# print(v2)
# print(m.check_con(v2, 1))
# print(m.eval_objs(v2))
# sa.run(m, 'from_hell', 100, 1000)
# mws.run(m,'from_hell', 100, 1000)


# Simple test to make sure that peg works
# m = model(decs_list, constraint_list, obs_list, True, False)
# v1 = m.gen_clean()
# print(v1)
# v2 = m.gen_spec(v1, 0)
# m.add_epsilon(0, v2, -10)
# print(v2)
# m.add_epsilon(0, v2, 10)
# print(v2)


