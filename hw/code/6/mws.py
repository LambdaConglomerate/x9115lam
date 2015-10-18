import model, random, sys

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

# Mutate one variable across its
# entire range, determining whether
# it has the best possible energy
def mutate(c, sn, m, energy):
  vect = sn
  e = energy(m, vect)
  # first set the chromosome to the minimum value
  vect[c] = m.get_min(c)
  step = 1.0/10.0
  max = m.get_max(c)
  for i in range(1, 10):
    m.add_epsilon(c, vect, max * step)
    if m.check_con(vect, c) and energy(m, vect) > e:
      sn = list(vect)
      e = energy(m, vect)
  return sn

def tweak(c, vect, m):
  tmp = list(vect)
  m.gen_spec(vect, c)
  capital = 5
  while not m.check_con(vect, c):
   # print('in tweak loop c is ' + str(c))
   # print "check con returns: " + str(m.check_con(vect, c))
   # print(vect)
   m.gen_spec(vect, c)
   capital -= 1
   if capital == 0: return tmp
  return vect

def add_vect(m, vect):
  resp = m.eval_objs(vect)
  # This works since the formula is
  # x = (x - min) / (max - min)
  # min is zero max is 2
  norm = lambda x: x / 2
  return norm(resp[0] + resp[1])

def from_hell(m, vect):
  resp = m.eval_objs(vect)
  dist_from_hell = ((1 - resp[0])**2 + (1 - resp[1])**2)**0.5
  return dist_from_hell / (2**(0.5))


# Pass in the model m
def run(m, e, retries, changes):
  print "RUN DATA: "
  print "Model: ", m.get_name()
  print "Optimizer: Max Walk Sat"

  emax = 1
  if e == 'from_hell':
    energy = from_hell
  else:
    energy = add_vect
  s = m.gen_con()
  print's is ',s
  e = energy(m, s)
  print 'starting s ', s
  print 'starting e ', e
  sb = s
  sbo = s
  eb = e
  ebo = e
  sn = sb
  for i in range(retries):
    print '\nT:', i
    for j in range(changes):
      # print 'S', s
      if e >= emax:
        print 'e was greater than e max'
        print 'e: ', e
        print 's: ', s
        return s,e
      c = random.randint(0, m.num_decs() - 1)
      if(random.random() >= 0.5):
        sn = tweak(c, sn, m)
      else:
        sn = mutate(c, sn, m, energy)
      en = energy(m, sn)
      if en > eb:
        sb = sn
        eb = en
        say("!")
      if en > e:
        say("+")
      else:
        say(".")
      s = list(sn)
      e = en
    # Print our best for that try
    print '\nSB:', sb
    print 'EB:', eb
    # First check if the sb for that set of changes was better
    # Than any of our other retries
    if(eb > ebo):
      sbo = list(sb)
      ebo = eb
    # Then retry with a brand new set of values
    s = m.gen_con()
    e = energy(m, s)
    sn = list(s)
    en = e
    sb = sn
    eb = en
  # If we're here we've run through all of our tries
  print '\n'
  print 'EBO ', ebo
  print 'SBO ', sbo
  print '\n'
  return sbo, ebo
