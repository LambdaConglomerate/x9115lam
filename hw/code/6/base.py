class base(object):
  def __init__(self, model):
    self.m = model

  def run(self):
    f1_obs = []
    f2_obs = []
    obs = []

    # Run the baseline model test 1000 times
    for j in range(10000):
      x = self.m.gen_con()
      print x
      y_list = self.m.eval_objs(x)

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
