import random, math, sys

def neighbor(m, id, vect, temp):
  epsilon = temp * random.random()
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

def run(m, e, retries, kmax):
  print "RUN DATA: "
  print "Model: ", m.get_name()
  print "Optimizer: Simulated Annealing"

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
    k = 1.0
    say("\n" + '(K:' + str(k) + ', SB:' + ''.join(["({0:.3f}) ".format(val) for val in sb]) + ', EB:(' + str(eb) + ')\t')
    while k < kmax and e < 1:
      c = random.randint(0, m.num_decs() - 1)
      sn = neighbor(m, c, s, (kmax - k)/kmax)
      # print 'sn ', sn
      en = energy(m, sn)

      # Is this a best overall?
      if en > eb:
        sb = sn
        eb = en
        say("!")

      # Is this better than where we were last?
      if en > e:
        s = sn
        e = en
        say("+")
      elif prob(e, en, k / kmax) < random.random():
        s = sn
        e = en
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
      sbo = sb
  print '\n\nSBO: ' + str(sbo)
  print 'EBO: ' + str(ebo) + '\n'


