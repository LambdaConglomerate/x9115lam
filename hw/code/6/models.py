import model, mws, sa, math
# OSYCKZYA STARTS HERE
def c0(args):
  # print 'args in c0 are ', args
  if(args[0] + args[1] - 2 < 0): return False
  if(6 - args[0] - args[1] < 0): return False
  if(2 - args[1] + args[0] < 0): return False
  return True
def c1(args):
  # print 'args in c1 are ', args
  if(4 - (args[2] - 3)**2 - args[3] < 0): return False
  return True
def c2(args):
  # print 'args in c2 are ', args
  if((args[4] - 3)**3 + args[5] - 4 < 0): return False
  return True

def f0(args):
  return -(25*(args[0]-2)**2 + (args[1] - 2)**2 + (args[2] - 1)**2 * (args[3]-4)**2 + (args[4] - 1)**2)
def f1(args):
  return args[0]**2 + args[1]**2 + args[2]**2 + args[3]**2 + args[4]**2 + args[5]**2

decs_list = (0,10), (0,10), (1,5), (0,6), (1,5), (0,10)
constraint_list = ((0,1),c0), ((2,3),c1), ((4,5),c2)
obs_list = (f0, (-640.908072277, -0.423436047808)), (f1, (25.4899157903, 176.005656027))

osyczka = model.model(decs_list, constraint_list, obs_list, True, True, "Osyczka2")

#SCHAFFER STARTS HERE
def f0(args):
  return args[0] * args[0]
def f1(args):
  return (args[0] - 2)**2

decs_list = ((-10**(5), 10**(5)),)
constraint_list = None
obs_list = (f0, (0, 10000000000)), (f1, (0, 9999600004))

schaffer = model.model(decs_list, constraint_list, obs_list, True, True, "Schaffer")

#KURSAWE STARTS HERE
# these are parameters used for a and b in the second objective
a_param = 1
b_param = 1
def f0(args):
  sum = 0
  sum += -10 * math.exp(-0.2*math.sqrt(args[0]**2 + args[1]**2))
  sum += -10 * math.exp(-0.2*math.sqrt(args[1]**2 + args[2]**2))
  return sum

def f1(args):
  sum = 0
  sum += abs(args[0])**a_param + 5 * math.sin(args[0])**b_param
  sum += abs(args[1])**a_param + 5 * math.sin(args[1])**b_param
  sum += abs(args[2])**a_param + 5 * math.sin(args[2])**b_param
  return sum

decs_list = (-5,5), (-5,5), (-5,5)
constraint_list = None
obs_list = (f0, (-19.8575351929, -4.98880272393)), (f1, (-10.587243916, 29.4348271457))

kursawe = model.model(decs_list, constraint_list, obs_list, True, True, "Kursawe")


model_list = [osyczka, schaffer, kursawe]
for m in model_list:
  for optimizer in [sa,mws]:
    optimizer.run(m, 'from_hell', 100, 1000)
