# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
import sys, random, math

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
- np: The number of candidates
- w: the influence of the current velocity
- phi_1: the social learning rate - how much you learn from other people
- phi_2: the cognitive learning rate - how much you learn from yourself
"""
def pso(model, retries, changes, goal = 0.01, pat = 100, era = 100, np=4, phi_1=2.8, phi_2=1.3):
    emin = 0
    # pulled K from the parameters, because it can be calculated from the
    # values for phi.
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    print 'k: ', k
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.1 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = list(init_pos)
    cans = [can(pos, vel, pbest) for pos, vel, pbest in zip(init_pos, init_vel, init_bpos)]
    # All the bests are the same here so what the hell right?
    glob_best = cans[0].pbest

    for c in cans:
        print c

    for c in cans:
        # I pulled out w.  If you look in off the shelf pso, it seems that it's kind of a one or the other
        # thing, either you use w or use K.  Look at the last page of off the shelf pso.
        c.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + (phi_2 * random.uniform(0,1) * (gbest - pos))) \
            for vel, pos, best, gbest in zip(c.vel, c.pos, c.pbest, glob_best)]
        # print 'c.vel', c.vel
        c.pos = [pos + vel for pos, vel in zip(c.pos, c.vel)]
        # NEED TO CHECK CONSTRAINTS/BOUNDS HERE SOMEWHERE BEFORE GOING ON TO THE NEXT CAN
        # print 'c.pos', c.pos

    for c in cans:
        print c
    best = cans[0].pos
    # We first check can zero's personal best
    # and update it if its current position
    # dominates.
    if model.cdom(best, cans[0].pbest):
        cans[0].pbest = list(best)
    # Could've done this with a for loop that
    # started at i = 1, but I'm an idiot so
    # I didn't do that.  I'm also stubborn
    # and this works.
    for i in xrange(len(cans) - 1):
        # We check each can as we go to see if
        # its current position dominates its
        # personal best
        if model.cdom(cans[i+1].pos, cans[0].pbest):
            cans[i+1].pbest = list(cans[i+1].pos)
        # This is where we're figuring out the
        # global best.
        if not model.cdom(best, cans[i+1].pos):
            #If we're here then we've been
            #bettered by the next can, so we
            #just set it to be our cursor
            best = list(cans[i+1].pos)
    # Once we make it out here we should have the
    # global best candidate.
    glob_best = best

    print 'glob_best ', glob_best
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
