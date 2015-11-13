# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
import sys, random, math, copy

class can(object):
    # Didn't want to override id so used uniq
    # as the variable.
    def __init__(self, pos, vel, pbest, uniq):
        self._pos = pos
        self._vel = vel
        self._pbest = pbest
        self._uniq = uniq

    def __str__(self):
        return "id: " + str(self._uniq) + "\npos: " + str(self._pos) + "\nvel: " + str(self._vel) + "\npbest: " + str(self._pbest) + '\n'

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
        return self._pbest
    @pbest.setter
    def pbest(self, vect):
        self._pbest = vect

    @property
    def uniq(self):
        return self._uniq

    @uniq.setter
    def uniq(self, uniq):
        self._uniq = uniq

def gens(model, np):
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.0 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = [list(x) for x in init_pos]
    init_ids = [i for i in xrange(np)]
    cans = [can(pos, vel, pbest, uniq) for pos, vel, pbest, uniq in zip(init_pos, init_vel, init_bpos, init_ids)]
    return cans

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
def pso(model, retries, changes, goal = 0.01, pat = 100, era = 100, np=30, phi_1=2.8, phi_2=1.3):
    emin = 0
    # pulled K from the parameters, because it can be calculated from the
    # values for phi.
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    s = gens(model, np)
    # Energy here is set to zero since we're not actively using it for now.
    st = state(model.name, 'PSO', s, 0, retries, changes, era)
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Model Name: ', model.name, '\nOptimizer: PSO'
    # Set an initial value for the global best
    # The downside to setting pbest equal to the current
    # particle position is that if there is a high phi_1 value
    # the particle will stay still until something happens globally
    # that pushes it away.
    st.sb = st.s[0].pbest
    #Initialize objective mins and maxs
    model.initializeObjectiveMaxMin(st.sb)
    tot_deaths = 0
    while st.t:
        st.k = changes
        patience = pat
        while st.k:
            # print "INITIAL CANS: "
            # for can in st.s:
            #     print 'can.pos: ', can.pos
            #     print 'can.pbest ', can.pbest
            num_deaths = 0
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest, st.sb)]
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                # Currently doing the same thing for particles that are
                # out of bounds and out of constraints, simply killing them
                # definitely some other options with this.  If they get to
                # bounds can set vector to boundary, and vel ot zero, then
                # just let them be pulled back into the space.
                if not model.checkBounds(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    num_deaths += 1
                if not model.checkConstraints(can.pos):
                    # print 'can ' + str(can.uniq) + ' died'
                    can.pos = model.retry()
                    # If this is zero something really weird happens
                    # there tends to be a can that will continue on
                    # having a zero velocity for a long period of time.
                    # REASON: If the can has a pbest that is its current
                    # position and our phi_1 is much higher than phi_2
                    # the particle will be attracted to its current position
                    # and may not break free for a long period of time.
                    can.vel = [0.0 for x in can.pos]
                    # Should a killed candidate maintain it's phantom memory?
                    # Uncomment this to wipe its memory.
                    # can.pbest = list(can.pos)
                    num_deaths += 1

                #Update objective maxs and mins    	
                model.updateObjectiveMaxMin(can.pos)
            tot_deaths += num_deaths
            # if num_deaths > 0:
            #     print "num deaths in era " + str(st.k) + " : " + str(num_deaths)
            # print "CANS AFTER MOVEMENT: "
            # for can in st.s:
            #     print 'can.pos: ', can.pos
            #     print 'can.pbest ', can.pbest
            # print 'GLOBAL BEST PRIOR TO DOM: ', st.sb
            print "======================="
            print "BEGIN DOM PROC K: ", st.k
            print "======================="
            best = st.s[0]
            for c in st.s:
                # print 'c id ', c.uniq
                # We first check the can's personal best
                # and update it if its current position
                # dominates.
                if model.cdom(c.pos, c.pbest, c):
                    # print "PBEST"
                    c.pbest = list(c.pos)
                for can in st.s:
                    if c == can:
                        continue
                    elif c.pos == can.pos:
                        print "PARTICLES IN SAME POSITION"
                        continue
                    if model.cdom(can.pos, c.pos, can, c):
                        #If we're here then we've been
                        #bettered by the next can, so we
                        #just set it to be our cursor
                        best = can
                # Once we make it out here we should have the
                # global best candidate.
                print 'best id after run ', best.uniq
                # print '+++++++++++++++++++++++++++'
                # print 'best pos after dom ', best.pos
            st.sb = best.pos
            st.eb = model.energy(st.sb)
            print 'final best id ', best.uniq
            # Looking at this just to make sure that
            # we are actually updating pbest.
            # print 'CANS AFTER DOM: '
            # for can in st.s:
            #    print can
            st.k -= 1
        # We need a clean slate here.
        print 'Global best: ', st.sb, 'global best energy: ', st.eb
        print 'Num deaths: ', tot_deaths
        print 'Total number of particles ', changes*np
        print "Attrition %0.2f percent" % (100.0 * (tot_deaths/(changes*np)))
        st.s = gens(model, np)
        st.sb = st.s[0].pbest
        st.t -= 1

    st.term()

