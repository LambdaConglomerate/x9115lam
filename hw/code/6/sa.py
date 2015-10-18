import random, math, sys

def neighbor(m, id, s, temp):
  vect = list(s)
  bound = m.get_bound(id)
  decay = math.exp(-temp)
  # temp is decreasing so the possibility
  # of a completely random position also is
  # decreasing.  If we miss this then we calculate
  # some epsilon based on the magnitude of the
  # difference between the max and min for the dec
  # and then add or subtract it
  if( random.random() < decay):
    # print 'vect id before ', vect[id]
    vect[id] = random.uniform(*bound)
    # print 'vect id after ', vect[id]
    # print 'm.check_con ', m.check_con(vect, id)
    if m.check_con(vect, id):
      return vect
    else:
      vect = list(s)
  mag = bound[1] - bound[0]
  # print 'bound', bound
  # print 'mag', mag
  # print 'temp', temp
  epsilon = decay * abs(mag)
  # print 'epsilon', epsilon

  add = bool(random.getrandbits(1))
  if add:
    m.add_epsilon(id, vect, epsilon)
  else:
    m.add_epsilon(id, vect, epsilon * -1)
  return vect

def say(x):
  sys.stdout.write(str(x)); sys.stdout.flush()

def prob(old, new, k):
  # print 'old is ', old
  # print 'new is ', new
  # print 'k is ',k
  x = math.exp(((new - old) / k))
  # print 'x in probability is ', x
  return x

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

def run(m, e, retries, kmax, goal = 0.01, pat = 10):
  print "\nRUN DATA "
  print "-------------------------"
  print "Model: ", m.get_name()
  print "Optimizer: Simulated Annealing"
  print 'Goal epsilon ', goal
  emax = 1
  if e == 'from_hell':
    energy = from_hell
  else:
    energy = add_vect

  sbo = None
  ebo = None
  for i in range(0,retries):
    s = m.gen_con()
    e = energy(m, s)
    sb = s
    eb = e
    eblast = e
    k = 1.0
    patience = kmax/pat
    say("\n" + '(K:' + str(k) + ', SB:' + ''.join(["({0:.3f}) ".format(val) for val in sb]) + ', EB:(' + str(eb) + ')\t')
    while k < kmax and e < emax:
      if emax - eb < goal:
        print '\n\nQuitting early, close enough.'
        print 'SB: ', sb
        print 'EB: ', eb
        print 'K: ', k
        return
      if eb == eblast:
        patience -= 1
        if patience <= 0:
          print '\nGot bored, nothing happening.'
          # print 'SB: ', sb
          # print 'EB: ', eb
          # print 'K: ', k
          break
      else:
        eblast = eb
        patience = kmax/pat
      c = random.randint(0, m.num_decs() - 1)
      sn = neighbor(m, c, s, k/kmax)
      # print 'sn ', sn
      en = energy(m, sn)

      # Is this a best overall?
      if en > eb:
        sb = list(sn)
        eb = energy(m, sb)
        say("!")

      # Is this better than where we were last?
      if en > e:
        s = list(sn)
        e = energy(m, s)
        say("+")
      elif prob(e, en, k / kmax) < random.random():
        s = list(sn)
        e = energy(m, s)
        say("?")
      else:
        say(".")
      k += 1.00

      if k % 50 == 0:
        say("\n" + '(K:' + str(k) + ', SB:' + ''.join(["({0:.3f}) ".format(val) for val in sb]) + ', EB:(' + str(eb) + ')\t')

    print '\nT: ' + str(i)
    print 'SB: ' + str(sb)
    print 'EB: ' + str(energy(m, sb))
    if not ebo or eb > ebo:
      ebo = eb
      sbo = list(sb)
  print '\n\nSBO: ' + str(sbo)
  print 'EBO: ' + str(ebo) + '\n'


