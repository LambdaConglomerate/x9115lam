payload = {
  "decs": {"x1":(0,10), "x2":(0,10), "x3":(1,5), "x4":(0,6), "x5":(1,5), "x6":(0,10)}
}

print payload


class model(object):

  def __init__(self, payload):
    self.decs = payload.get("decs") if payload else None
    self.objs = payload.get("objs") if payload else None
    self.energy = payload.get("energy") if payload else None
    self.constraints = payload.get("constraints") if payload else None

  def genVals():
