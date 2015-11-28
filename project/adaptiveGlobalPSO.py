# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
from grapher import *
import sys, random, math, copy



def gens(model, np):
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.0 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = [list(x) for x in init_pos]
    init_ids = [i for i in xrange(np)]
    cans = [can(pos, vel, pbest, uniq) for pos, vel, pbest, uniq in zip(init_pos, init_vel, init_bpos, init_ids)]
    return cans

def addToFront(model, frontier, pos):
    nondom = True
    for fpos in frontier:
        ret_val = model.cdom(pos, fpos)
        if ret_val == -1:
            continue
        elif ret_val == 1:
            fpos = pos
            nondom = False
            break
        else:
            nondom = False
            break
    if nondom:
        frontier.append(pos)

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
def adaptiveGlobalPSO(model, retries, changes, graph=False, goal = 0.01, pat = 100, \
    era = 100, np=30, phi_1=2.5, phi_2=1.5):
    emin = 0
    # pulled K from the parameters, because it can be calculated from the
    # values for phi.
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    s = gens(model, np)
    #initialize grapher
    if graph:
        g = grapher(model, np)
        for can in s:
            g.addVector(can.pos, can.uniq)
    # Energy here is set to zero since we're not actively using it for now.
    st = state(model.name, 'adaptiveGlobalPSO', s, 0, retries, changes, era)
    # print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    # print 'Model Name: ', model.name, '\nOptimizer: Adaptive Global PSO, K: ', changes
    # Set an initial value for the global best
    # The downside to setting pbest equal to the current
    # particle position is that if there is a high phi_1 value
    # the particle will stay still until something happens globally
    # that pushes it away.
    st.sb = st.s[0].pos
    st.sblast = st.s[0].pos
    bestcan = st.s[0]
    # # #Initialize objective mins and maxs
    # model.initializeObjectiveMaxMin(st.sb)
    # # #we whould do this just in case
    # for c in st.s:
    #     model.updateObjectiveMaxMin(c.pos)
    tot_deaths = 0
    # The frontier is just a list
    # of positions, not cans!
    frontier = list()
    while st.t:
        # Print a dot at the beginning of each retry
        # just to show that something is happening.
        print "."
        # #Initialize objective mins and maxs
        # model.initializeObjectiveMaxMin(st.sb)
        # #we whould do this just in case
        # for c in st.s:
            # model.updateObjectiveMaxMin(c.pos)
        st.k = changes
        patience = pat
        while st.k:
            # if st.sb == st.sblast:
            #     patience -= 1
            #     if patience == 0:
            #         st.bored()
            #         break
            num_deaths = 0
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + \
                 (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest, st.sb)]
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                # Currently doing the same thing for particles that are
                # out of bounds and out of constraints, simply killing them
                # definitely some other options with this.  If they get to
                # bounds can set vector to boundary, and vel ot zero, then
                # just let them be pulled back into the space.
                if not model.checkBounds(can.pos) or not model.checkConstraints(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    # Should a killed candidate maintain it's phantom memory?
                    # Uncomment this to wipe its memory.
                    # can.pbest = list(can.pos)
                    num_deaths += 1
                #Update objective maxs and mins
                if graph:
                    g.addVector(can.pos, can.uniq)
                # model.updateObjectiveMaxMin(can.pos)
            tot_deaths += num_deaths
            #if you want to see step by step particle movement uncomment below
            #warning you will end up having to terminate this manually
            #g.graph()
            for i in xrange(len(st.s) - 1):
                pbret = model.cdom(st.s[i].pos, st.s[i].pbest, st.s[i], st.s[i])
                if pbret == 0 or pbret == -1:
                    st.s[i].pbest = list(st.s[i].pos)
                ret_val = model.cdom(st.sb, st.s[i+1].pos, bestcan, st.s[i+1])
                if ret_val == 0:
                    st.sb = st.s[i+1].pos
                    st.sblast = st.s[i+1].pos
                    bestcan = st.s[i+1]
                elif ret_val == -1:
                    addToFront(model, frontier, st.s[i+1].pos)
            if not st.sb in frontier:
                addToFront(model, frontier, st.sb)
            st.k -= 1
        # We need a clean slate here.
        # print '++++++++++++++++++++++++++++++++++++++++++++++++++++'
        # print 'Global best: ', st.sb, '\nGlobal best energy: ', st.eb
        # print 'Num deaths: ', tot_deaths
        # print 'Total number of particles ', changes*np
        # print "Attrition %0.2f percent" % (100.0 * (tot_deaths/(changes*np)))
        # for can in st.s:
        #     addToFront(model, frontier, can.pbest)
        f = [model.cal_objs_2(pos) for pos in frontier]
        st.addFrontier(f)
        st.s = gens(model, np)
        st.sb = st.s[0].pbest
        st.sblast = st.s[0].pbest
        bestcan = st.s[0]
        st.t -= 1
    if graph:
        g.graph()
        g.graphEnergy()
    st.termPSO()
