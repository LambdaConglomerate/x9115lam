import random, math, sys

s0 = (0, 0)
k_max = 10000
epsilon = 0.01

def schaffer(f1, f2):
  f1 = f1*f1
  f2 = (f2 - 2) * (f2 - 2)
  return f1 + f2

def normalization(f1, f2):
  return ((f1+f2) - 0) / (1 - 0)
  
def base_runner():
  # list of minimum observations for 100 iterations
  # of the model being run 100 times each
  min_obs = []
  # list of max observations for 100 iterations
  # of the model being run 100 times each
  max_obs = []
  
  # list of the energies for 100 iterations
  # of the model being run 100 times each
  max_energies = []

  # Run the baseline model test 100 times
  for i in range(100):
    # observations for each run
    obs = []
    # Run the model 100 times
    for j in range(100):
      f1 = random.random()
      f2 = random.random()
      obs.append((f1,f2, schaffer(f1,f2)))
      
    # Sort by the schaffer value
    obs = sorted(obs, key=lambda ob: ob[2])

    # Add the min and max of this run
    min_obs.append(obs[0])
    max_obs.append(obs[-1])

  min_obs = sorted(min_obs, key=lambda ob: ob[2])
  max_obs = sorted(max_obs, key=lambda ob: ob[2])
  
  global min, max
  
  min = min_obs[0][2]
  max = max_obs[-1][2]
  
   # Run the baseline model test 100 times
  for i in range(100):
    # energies for each run
    energies = []
    # Run the model 100 times
    for j in range(100):
      f1 = random.random()
      f2 = random.random()
      energies.append((f1, f2, energy(f1, f2, schaffer)))

    # Sort by the schaffer value
    energies = sorted(energies, key = lambda en: en[2])

    # Add the max energy of this run
    max_energies.append(energies[-1])
  
  max_energies = sorted(max_energies, key = lambda en: en[2])
  
  global e_max
  
  e_max = max_energies[-1][2]

  print 'median min observation: ' + str(min_obs[49][0]) + '\t' + str(min_obs[49][1]) + '\t' + str(min_obs[49][2])
  print 'median max observation: ' + str(max_obs[49][0]) + '\t' + str(max_obs[49][1]) + '\t' + str(max_obs[49][2])
  print 'abs min observation: ' + str(min_obs[0][0]) + '\t' + str(min_obs[0][1]) + '\t' + str(min_obs[0][2])
  print 'abs max observation: ' + str(max_obs[-1][0]) + '\t' + str(max_obs[-1][1]) + '\t' + str(max_obs[-1][2])
  print 'max energy: ' + str(max_energies[-1][0]) + '\t' + str(max_energies[-1][1]) + '\t' + str(max_energies[-1][2])
  
def energy(f1, f2, func):
  func_val = func(f1, f2)
  return (func_val - min) / (max - min)
  
def neighbor(s):
  add_f1 = bool(random.getrandbits(1))
  add_f2 = bool(random.getrandbits(1))
  if add_f1:
    f1_delta = epsilon
  else:
    f1_delta = -epsilon
    
  if add_f2:
    f2_delta = epsilon
  else:
    f2_delta = -epsilon
    
  return (s[0] + f1_delta, s[1] + f2_delta)
  
def prob(old, new, k):
  t = 1 - (k/k_max)
  return math.exp(-1*(new - old)/t)

def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()
  
def sim_anneal(func):
  s = s0
  e = energy(s[0], s[1], func)
  print e
  sb = s
  eb = e
  k = 0
  #print "Initial setup (s, e, e_max, sb, eb, k, k_max): ", s, e, e_max, sb, eb, k, k_max
    
  while k < k_max and e < e_max:
    sn = neighbor(s)
    en = energy(sn[0], sn[1], func)
    
    if en < eb:
      sb = sn
      eb = en
      say("!")
    
    if en < e:
      s = sn
      e = en
      say("+")
    elif prob(e, en, (1-k)/k_max) > random.random():
      s = sn
      e = en
      say("?")
    
    say(".")
    k = k + 1
      
    if k % 50 == 0:
      say("\n" + "({0:.3f},{0:.3f})".format(sb[0], sb[1]))
    
if __name__ == "__main__":
  base_runner()
  sim_anneal(schaffer)
