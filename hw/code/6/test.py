def bounds(min, max):
  def f(rand):
    return ((max-min) * rand) + min
  return f

def constraints():
  def f(*args):
    if(args[0] + args[1] - 2 < 0): return False
    if(6 - args[0] - args[1] < 0): return False
    if(2 - args[1] + args[0] < 0): return False
    if(4 - (args[2] - 3)**2 - args[3] < 0): return False
    if((args[4] - 3)**3 + args[5] - 4 < 0): return False
    return True
  return f

def osyczka2():
  def f(*args):
    f1 = -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
    f2 = args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2
    return (f1, f2)
  return f

payload = {
  "decs": {"x1":bounds(0,10), "x2":bounds(0,10), "x3":bounds(1,5), "x4":bounds(0,6), "x5":bounds(1,5), "x6":bounds(0,10)},
  "objectives": osyczka2(),
  "constraints": constraints()
}

print(payload)
