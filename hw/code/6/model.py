import random, math, sys
class model(object):

  def __init__(self, payload):
    self.decs = payload.decs if payload else None
    self.objs = payload.objs if payload else None
    # self.energy = payload.energy if payload else None
    self.constraints = payload.cons if payload else None

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

  def gen_con(self, vector=None):
    if not vector:
      vector = self.gen_clean()
    for c in self.constraints:
      while not c.state(vector):
        # print('c is', c)
        vector = self.gen_spec(c.ids, vector)
    return vector

  def eval_objs(self, vector):
    eval_list = []
    for f in self.objs:
      eval_list.append(f(vector))
    # print(eval_list)
    return eval_list
