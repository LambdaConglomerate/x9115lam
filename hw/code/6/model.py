import random, math, sys
class model(object):

  def __init__(self, payload=None):
    self.decs = payload.decs if payload else None
    self.objs = payload.objs if payload else None
    self.constraints = payload.cons if payload else None
    self.bound = payload.bound if payload else None
    if payload.energy == 'from_hell':
      self.energy = self.from_hell()
    elif payload.energy == 'add_vect':
      self.energy = self.add_vect()
    else:
      self.energy = None

  # Never use directly, only use
  # check_con which calls this
  # function when needed.  Also
  # check con knows whether there
  # are constraints or not.
  def gen_clean(self):
    vector = []
    count = 0
    for dec in self.decs:
      vector.append(dec(random.random()))
      count += 1
    # print vector
    return vector

  def gen_spec(self, ids, vector):
    for id in ids:
      # print('id ', id)
      # print('vector b/4 ', vector)
      func = getattr(self.decs, id)
      vector[int(id[1:]) - 1] = func(random.random())
      # print('vector after ', vector)
    return vector

  # This approach might really not work
  # forever.
  # Additionally this assumes that each decision
  # is only involved in one set of constraints.
  # If that isn't true we need to make changes here.
  def check_con(self, vector, id):
    for c in self.constraints:
      # print c
      # print c.ids
      for i in c.ids:
        if id == i:
          return(c.state(vector))
    # This should never happen, but if it does
    # we will know something is wrong.
    return None

  def gen_con(self, vector=None):
    # If we don't have any constraints
    # we don't need to do anything
    # other than regen a new vector
    if self.constraints == None:
      vector = self.gen_clean()

    if not vector:
      vector = self.gen_clean()
    for c in self.constraints:
      while not c.state(vector):
        # print('c is', c)
        vector = self.gen_spec(c.ids, vector)
    return vector

  def eval_objs(self, vector):
    eval_list = []
    #print self.objs
    for f in self.objs:
      # print f
      if(self.bound):
        not_norm = f.func(vector)
        norm = f.norm(not_norm)
        # print 'not_norm ', not_norm
        # print 'norm ', norm
        eval_list.append(norm)
      else:
        eval_list.append(f(vector))
    print 'f1: ', eval_list[0]
    print 'f2: ', eval_list[1]
    return eval_list

  # Simple normalization function to
  # normalize (b1, b2) to range (0,1).
  def normalize(b1, b2):
    def n(x):
      return (x - b1) / (b2 - b1)
    return n

  # Add f1 and f2 and then normalize
  # range [0,2] to (0,1)
  def add_vect(self):
    def func(vector):
      resp = self.eval_objs(vector)
      norm = normalize(0, 2)
      return norm(resp[0] + resp[1])
    return func

  # Calculate distance from (1,1) and then normalize range
  # [0,sqrt(2)] to (0,1)
  def from_hell(self):
    def func(vector):
      resp = self.eval_objs(vector)
      dist_from_hell = ((1 - resp[0])**2 + (1 - resp[1])**2)**0.5
      return dist_from_hell / (2**(0.5))
    return func
