# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
from grapher import *
import sys, random, math, copy


class can(object):
    # Didn't want to override id so used uniq
    # as the variable.
    def __init__(self, pos, vel, pbest, uniq, radius):
        self._pos = pos
        self._vel = vel
        self._pbest = pbest
        self._uniq = uniq
        #this could also be charge
        self._weight = 1.0
        self._radius = radius

    def __str__(self):
        return "id: " + str(self._uniq) + "\npos: " + str(self._pos) + "\nvel: " + str(self._vel) + "\npbest: " + str(self._pbest) + '\n'

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, vect):
        self._pos = vect

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
    
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight):
        self._weight = weight

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

def gens(model, np, radius):
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.0 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = [list(x) for x in init_pos]
    init_ids = [i for i in xrange(np)]
    cans = [can(pos, vel, pbest, uniq, radius) for pos, vel, pbest, uniq in zip(init_pos, init_vel, init_bpos, init_ids)]
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
- inertia: controls the momentum of the particle
"""

#euclidean distance
def distance(v1, v2):
    return sum([(a + b)**2.0 for a, b in zip(v1, v2)])**(1/2.0)

#calculate repulsion
def repulsion(c1, c2, radius):
    #coulomb's law, tinker with constant
    constant = 1.0
    force = constant * c1.weight * c2.weight / (radius**2.0)
    return force


#basically if two vectors are within some distance of each other they combine
#with weights added together
#otherwise they will repulse each other based on their weights
#and coulomb's law
def classicalGlobalPSOV2(model, retries, changes, goal = 0.01, pat = 100, era = 100, np=30, phi_1=2.8, phi_2=1.3, inertia=0.8):
    emin = 0

    #setting vmax to full search range for an particle (from lit)
    # val bounds = [model.getBounds(i) for i in range(model.numOfDecisions())][0]
    # val difference 
    vmax = max([(x[1] - x[0]) for x in [model.getBounds(i) for i in range(model.numOfDecisions())]])

    radius = vmax * 0.01;
    
    s = gens(model, np, radius)
    #initialize grapher
    g = grapher(model, np)
    for can in s:
        g.addVector(can.pos, can.uniq)
    # Energy here is set to zero since we're not actively using it for now.
    st = state(model.name, 'classicalGlobalPSOV2', s, 0, retries, changes, era)
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    print 'Model Name: ', model.name, '\nOptimizer: Classical Global PSO V2, K: ', changes
    # Set an initial value for the global best
    # The downside to setting pbest equal to the current
    # particle position is that if there is a high phi_1 value
    # the particle will stay still until something happens globally
    # that pushes it away.
    st.sb = st.s[0].pbest
    #Initialize objective mins and maxs
    model.initializeObjectiveMaxMin(st.sb)
    #we whould do this just in case
    for c in st.s:
        model.updateObjectiveMaxMin(c.pos)
    tot_deaths = 0
    while st.t:
        st.k = changes
        patience = pat
        while st.k:
            num_deaths = 0
            for can in st.s:
                can.vel =  [inertia * vel + (phi_1 * random.uniform(0,1) * (best - pos)) + (phi_2 * random.uniform(0,1) * (gbest - pos)) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest, st.sb)]
                #checking if velocity is at max
                can.vel = [vmax if vel > vmax else vel for vel in can.vel]
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                
                # Currently doing the same thing for particles that are
                # out of bounds and out of constraints, simply killing them
                # definitely some other options with this.  If they get to
                # bounds can set vector to boundary, and vel ot zero, then
                # just let them be pulled back into the space.
                if not model.checkBounds(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    # Should a killed candidate maintain it's phantom memory?
                    # Uncomment this to wipe its memory.
                    # can.pbest = list(can.pos)
                    num_deaths += 1
                if not model.checkConstraints(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    # Should a killed candidate maintain it's phantom memory?
                    # Uncomment this to wipe its memory.
                    # can.pbest = list(can.pos)
                    num_deaths += 1
                #Update objective maxs and mins
                g.addVector(can.pos, can.uniq)
                model.updateObjectiveMaxMin(can.pos)

            #logic for dealing with collision and combining
            #particles
            for c in st.s:
                for can in st.s:
                    if c == can:
                        continue
                    else:
                        radius = distance(c.pos, can.pos)
                        #if we are within the particles gravitational pull
                        #combine into one particle
                        if radius < max(c.radius, can.radius):
                            #the particle with better energy 
                            #becomes the final particle
                            #we delete the particle with worse energy
                            if model.energy(c.pos) < model.energy(can.pos):
                                c.weight = c.weight + can.weight
                                c.radius = c.radius + can.radius
                                del(can)
                            else:
                                can.weight = can.weight + c.weight
                                c.radius = c.radius + can.radius
                                del(c) 
                        else:
                            #here we repulse if we are outside
                            #the radius of gravitation for the
                            #particles
                            repulsedVelocity = repulsion(c, can, radius)
                            can.vel = [repulsedVelocity * vel + inertia * vel for vel in can.vel]
                            can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                            #instead of resetting wiggle 
                            #each index until bounds and constraints
                            #are met
                            for i in xrange(len(can.pos)):
                                can.pos = model.singleRetry(can.pos, i)

                            #other particle will repulse the opposite direction    
                            c.vel = [-repulsedVelocity * vel + inertia * vel for vel in c.vel]
                            c.pos = [pos + vel for pos, vel in zip(c.pos, c.vel)]
                            for i in xrange(len(c.pos)):
                                c.pos = model.singleRetry(can.pos, i)

            tot_deaths += num_deaths
            #if you want to see step by step particle movement uncomment below
            #warning you will end up having to terminate this manually
            #g.graph()
            # print "======================="
            # print "BEGIN DOM PROC K: ", st.k
            # print "======================="
            best = st.s[0]
            best_list = []
            low_diff = []
            for c in st.s:
                best = c
                # print 'c is ', c.uniq
                # We first check the can's personal best
                # and update it if its current position
                # dominates.
                if model.cdom(c.pos, c.pbest, c):
                    c.pbest = list(c.pos)
                for can in st.s:
                    if c == can:
                        continue
                    elif c.pos == can.pos:
                        # print "PARTICLES IN SAME POSITION"
                        continue
                    # If we're at this point then the particles
                    # aren't exactly equal in position, and also
                    # aren't the same particle.
                    diff = sum([math.fabs(x-y) for x,y in zip(c.pos, can.pos)])
                    # if diff < 1:
                    #     # print 'diff: ', diff, ' particle ids: ', c.uniq, can.uniq
                    #     low_diff.append((c.uniq, can.uniq))
                    if model.cdom(can.pos, best.pos, can, best):
                        #If we're here then we've been
                        #bettered by the next can, so we
                        #just set it to be our cursor
                        best = can
                # Once we make it out here we should have the
                # global best candidate.
                if(not best.uniq in best_list):
                    best_list.append(best.uniq)
                # print 'best id after run ', best.uniq
            st.sb = best.pos
            st.eb = model.energy(st.sb)
            # print 'low diff list ', low_diff
            # print 'best_list ', best_list
            st.k -= 1
        # We need a clean slate here.
        # print '++++++++++++++++++++++++++++++++++++++++++++++++++++'
        # print 'Global best: ', st.sb, '\nGlobal best energy: ', st.eb
        # print 'Num deaths: ', tot_deaths
        # print 'Total number of particles ', changes*np
        # print "Attrition %0.2f percent" % (100.0 * (tot_deaths/(changes*np)))
        #st.s = gens(model, np)
        st.sb = st.s[0].pbest
        st.t -= 1
    g.graph()
    g.graphEnergy()
    st.term()
