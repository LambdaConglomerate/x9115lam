import random

def shaffer(f1, f2):
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

  # Run the baseline model test 100 times
  for i in range(100):
    # observations for each run
    obs = []
    # Run the model 100 times
    for j in range(100):
      f1 = random.random()
      f2 = random.random()
      obs.append((f1,f2, shaffer(f1,f2)))

    # Sort by the shaffer value
    obs = sorted(obs, key=lambda ob: ob[2])

    # Add the min and max of this run
    min_obs.append(obs[0])
    max_obs.append(obs[-1])

  min_obs = sorted(min_obs, key=lambda ob: ob[2])
  max_obs = sorted(max_obs, key=lambda ob: ob[2])

  print 'median min observation: ' + str(min_obs[49][0]) + '\t' + str(min_obs[49][1]) + '\t' + str(min_obs[49][2])
  print 'median max observation: ' + str(max_obs[49][0]) + '\t' + str(max_obs[49][1]) + '\t' + str(max_obs[49][2])
  print 'abs min observation: ' + str(min_obs[0][0]) + '\t' + str(min_obs[0][1]) + '\t' + str(min_obs[0][2])
  print 'abs max observation: ' + str(max_obs[-1][0]) + '\t' + str(max_obs[-1][1]) + '\t' + str(max_obs[-1][2])

base_runner()
