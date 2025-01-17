import logging, sys

"""
  Parameters:
  - model_name: The name of the model you're running
  - optimizer:  The name of the optimizer you're running
  - s:          Your initial candidate vector.
  - energy:     The energy of the initial candidate vector.
  - retries:    The number of retries to run the optimizer
  - changes:    The number of iterations to run the optimizer for on each retry
  - era:        This is essentially the verbosity level.  We print out the energy, and solution
                every time that k mod era is equal to zero.
  - out:        The ouptut file.  If you overide the default run.sh won't work.
  - log_level:  If this is anything other than debug only the info logs will be spit out.
"""
class state(object):
  def __init__(self, model_name, optimizer, s, energy, retries, changes, era, out='out.txt', log_level=None):
    self.name = model_name
    self.optimizer = optimizer
    self._e = energy
    self._eb = energy
    self._ebo = energy
    self.en = energy
    self.eblast = energy
    self._s = list(s)
    self._sb = list(s)
    self._sbo = list(s)
    self.sn = list(s)
    self._t = retries
    self._k = changes
    self.era = era
    if log_level == 'debug':
      logging.basicConfig(filename=out, format='%(message)s',level=logging.DEBUG)
    else:
      logging.basicConfig(filename='out.txt', format='%(message)s',level=logging.INFO)
    self.logger = logging.getLogger('State')
    self.logger.info("%s\nModel: %s\nOptimizer: %s\nNum Retries: %s\nNum Changes: %s\nInitial S: %s\nInitial E: %0.3f\n%s" % \
      ('-'*100, self.name, self.optimizer, self._t, self._k, self._s, self._e, '-'*100))
    self.outstring = ""

  def __str__(self):
    if self._e == self._eb == self._ebo:
      return "%s\nModel: %s\n\nNum Retries: %s\nNum Changes: %s\nInitial S: %s\nInitial E: %0.3f\n%s\n" % \
      ('-'*100, self.name, self._t, self._k, self._s, self._e, '-'*20)
    else:
      return "T:%d\tK:%d\tS:%s\tE:%0.3f\n" % (self._t, self._k, self._s, self._e)

  def term(self):
    if self.outstring != "":
      self.logger.info(self.outstring)
      self.outstring =""
    self.logger.info("\nFINAL:\nMODEL:%s\nOPTIMIZER:%s\nEBO:%0.3f\tSBO:%s\n" % \
      (self.name, self.optimizer, self._ebo, self._sbo))

  def bored(self):
    self.app_out("\ngot bored at K:%d" % (self._k))

  def app_out(self, char):
    self.outstring += char

  @property
  def t(self):
    """ The retry property. """
    return self._t
  @t.setter
  def t(self, val):
    self._t = val
    if self.outstring != "":
      self.logger.info(self.outstring)
      self.outstring =""
    if self._t != 0:
      self.logger.info("\n%s\nT:%d\tK:%d\tEBO:%0.3f\tSBO:%s\n%s" % \
        ('-'*100, self._t, self._k, self._ebo, self._sbo, '-'*100))

  @property
  def k(self):
    """ The iteration number property. """
    return self._k
  @k.setter
  def k(self, val):
    self._k = val
    if self._k % self.era == 0 and self._k != 0:
      self.logger.info(self.outstring)
      self.outstring = ""
      self.logger.info("K:%d\tEB:%0.3f\tSB:%s" % \
        (self._k, self._eb, self._sb))

  @property
  def e(self):
    """ The energy property. """
    return self._e
  @e.setter
  def e(self, val):
    self._e = val
    self.logger.debug("T:%d\tK:%d\tE:%0.3f\tS:%s" % \
      (self._t, self._k, self._e, self._s))

  @property
  def eb(self):
    """ The energy best property. """
    return self._eb
  @eb.setter
  def eb(self, val):
    self._eb = val
    self.logger.debug("T:%d\tK:%d\tEB:%0.3f\tSB:%s" % \
      (self._t, self._k, self._eb, self._sb))

  @property
  def ebo(self):
    """ The energy best overall property. """
    return self._ebo
  @ebo.setter
  def ebo(self, val):
    self._ebo = val
    self.logger.debug("T:%d\tK:%d\tEBO:%0.3f\tSBO:%s" % \
      (self._t, self._k, self._ebo, self._sbo))

  @property
  def s(self):
    """ The candidate property. """
    return self._s
  @s.setter
  def s(self, val):
    self._s = list(val)

  @property
  def sb(self):
    """ The best candidate property. """
    return self._sb
  @sb.setter
  def sb(self, val):
    self._sb = list(val)

  @property
  def sbo(self):
    """ The best candidate overall property. """
    return self._sbo
  @sbo.setter
  def sbo(self, val):
    self._sbo = list(val)

