import model, random, sys

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

# Mutate one variable across its
# entire range, determining whether
# it has the best possible energy
def mutate(c, sn, m):
  vect = list(sn)
  e = m.energy(sn)
  id = 'x' + str(c)
  # print 'id is in mutate: ' + id
  #for the each tenth go through bounds of the decision
  for i in range(1, 10):
    step = getattr(m.decs, id)(i/10.0)
    # Need this to be c minus 1 since we're
    # returning in a 1 based range on line 53
    # to make it simpler to get the id
    vect[c - 1] = step
    # The indexing using the named tuple cleans this
    # up significantly.  Check con just needs the id
    # to find the constraints for this variable.
    if m.check_con(vect, id) and m.energy(vect) > e:
      # using sn here, if  nothing is better than
      # what was in sn before we just return sn
      sn = list(vect)
      e = m.energy(vect)
  return sn

def tweak(c, sn, m):
    id = 'x' + str(c)
    # print 'id is in tweak: ', id
    # print 'sn is ', sn
    sn_temp = sn
    # Need this to be c minus 1 since we're
    # returning in a 1 based range on line 53
    # to make it simpler to get the id
    sn_temp[c - 1] = getattr(m.decs, id)(random.random())
    # we try ten times to make this work, if we fail then
    # we just leave sn alone and return it as it was
    # count = 0
    while not m.check_con(sn, id):
      sn_temp[c - 1] = getattr(m.decs, id)(random.random())
      # count += 1
    # print 'final sn is ', sn_temp
    # print 'count in tweak: ' + str(count)
    return sn_temp

# Pass in the model m
def run(m):
  max_changes = 1000
  max_retries = 1000
  emax = 1
  s = m.gen_con()
  e = m.energy(s)
  print 'starting s ', s
  print 'starting e ', e
  sb = s
  sbo = s
  eb = e
  ebo = e
  sn = sb
  for i in range(max_retries):
    print '\nT:', i
    for j in range(max_changes):
      # print 'S', s
      if e >= emax:
        print 'e was greater than e max'
        print 'e: ', e
        print 's: ', s
        print 'constraint 1 ', m.check_con(s, 'x' + str(1))
        print 'constraint 2 ', m.check_con(s, 'x' + str(3))
        print 'constraint 3 ', m.check_con(s, 'x' + str(5))
        return s,e
      #pick the x to mutate
      num_decs = len(m.decs)
      c = random.randint(1, num_decs)
      if(random.random() >= 0.5):
        sn = tweak(c, sn, m)
      else:
        sn = mutate(c, sn, m)
      en = m.energy(sn)
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
    e = m.energy(s)
    sn = list(s)
    en = e
    sb = sn
    eb = en
  # If we're here we've run through all of our tries
  print '\n'
  print 'EBO ', ebo
  print 'SBO ', sbo
  return sbo, ebo
