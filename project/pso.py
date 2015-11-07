# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
import sys, random

class can(object):
    def __init__(self, pos, vel, pbest):
        self._pos = pos
        self._vel = vel
        self._pbest = pbest

    def __str__(self):
        return "pos: " + str(self._pos) + "\nvel: " + str(self._vel) + "\npbest: " + str(self._pbest) + '\n'

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, vect):
        self._pos = vect

    @property
    def vel(self):
        return self._vel
    @vel.setter
    def vel(self, vect):
        self._vel = vect

    @property
    def pbest(self):
        return self._pos
    @pbest.setter
    def pbest(self, vect):
        self._pbest = vect

"""
Parameters:
- model: The model you want to run.
- retries: The number of times to completely restart from scratch with
  a totally random vector.
- changes: The number of times to actually run the optimizer for each retry
- goal: This is an epsilon value.  If the energy value is within this amount
  of the minimum/maximum energy then we decide its good enough and stop.
- pat: This is our patience for finding a solution.  If we see the same
  energy best value 100 times in a row we give up.  If somewhere in our
  countdown we actually find a new best we reset the patience to its original
  value again.
- era: This is basically a pass through to the state of the optimizer. It determines
  how often we will print an output line giving the best energy and best solution so far.
"""
def pso(model, retries, changes, goal = 0.01, pat = 100, era = 100, np=30, K=0.0885, w=1, phi_1=2.8, phi_2=1.3):
    emin = 0
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [0.0 for x in xrange(np)]
    init_bpos = list(init_pos)
    cans = [can(pos, vel, pbest) for pos, vel, pbest in zip(init_pos, init_vel, init_bpos)]
    for c in cans:
        print c

    # model.initializeObjectiveMaxMin(s)
    # for i in xrange(1000):
    #     # prime the maxs and mins with second values, avoids divide by 0
    #     model.updateObjectiveMaxMin(model.retry())
    # st = state(model.name, 'PSO', s, model.energy(s), retries, changes, era)
    # print 'model name ', model.name, 'optimizer', 'PSO'
    # #changes is some static value passed by the caller
    # #st changes is actually a counter
    # while st.t:
    #     st.k = changes
    #     patience = pat

    #     while st.k:

    #         st.k -= 1
    #     # First check if the sb for that set of changes was better
    #     # Than any of our other retries
    #     if(st.eb < st.ebo):
    #         st.app_out(' ^')
    #         st.sbo = list(st.sb)
    #         st.ebo = st.eb
    #     # Then retry with a brand new set of values
    #     st.s = model.retry()
    #     st.e = model.energy(st.s)
    #     st.sn = list(st.s)
    #     st.en = st.e
    #     st.sb = list(st.sn)
    #     st.eb = st.en
    #     st.t -= 1
    # st.term()
