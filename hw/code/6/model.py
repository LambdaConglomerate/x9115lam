import random, math, sys
class model(object):

  def __init__(self, payload):
    self.decs = payload.get("decs") if payload else None
    self.objs = payload.get("objs") if payload else None
    self.energy = payload.get("energy") if payload else None
    self.constraints = payload.get("constraints") if payload else None

  def regen(self):
    vector = []
    count = 0
    for k,v in sorted(self.decs.iteritems()):
      vector.append(v(random.random()))
      count += 1
    return vector

  def gen_vals(self):
    vector = self.regen()
    if(self.constraints):
      count = 0
      while(not self.constraints(vector)):
        print('out of constraint')
        print(vector)
        count += 1
        vector = self.regen()
      print("final count", count)

