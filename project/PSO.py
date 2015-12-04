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

def PSO(model, retries, changes, graph=False, goal = 0.01, pat = 100, \
era = 100, np=30, phi_1=2.8, phi_2=1.2):
    # g = grapher(model, int(retries))
    emin = 0
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    s = gens(model, np)
    st = state(model.name, 'adaptiveGlobalPSO', s, 0, retries, changes, era)
    st.sb = st.s[0].pos
    bestcan = st.s[0]
    tot_deaths = 0
    #retry loop
    while st.t:
        print "."
        model.initializeObjectiveMaxMin(st.sb)
        for c in st.s:
            model.updateObjectiveMaxMin(c.pos)
        st.k = changes
        #iterative loop
        while st.k:
            num_deaths = 0
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + \
                 (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest, st.sb)]
                # print 'can.vel ', can.vel
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                if not model.checkBounds(can.pos) or not model.checkConstraints(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    num_deaths += 1
                model.updateObjectiveMaxMin(can.pos)
            tot_deaths += num_deaths
            print "="*29
            print "k ", st.k
            # print "tot_deaths ", tot_deaths
            runDom(st, model)
            st.k -= 1
        st.s = gens(model, np)
        st.sb = st.s[0].pbest
        bestcan = st.s[0]
        st.t -= 1
    # g.graph()
    # g.graphEnergy()
    st.termPSO()


def findEpsilon(model, setOfPos):
    k = 1.0
    objs = [model.cal_objs(pos) for pos in setOfPos]
    print objs
    scoreList = list()
    ob3Max = None
    for i in xrange(len(objs)):
        diffVect = [[objs[i][k] - objs[j][k] for k in xrange(len(objs[i])) if j != i] for j in xrange(len(objs)) if j != i]
        diffList = [max(v) for v in diffVect]
        # print 'diffList ', diffList
        # print "len ", len(diffList)
        diffListExpo = [-math.exp(-val/k) for val in diffList]
        # print 'diffListExpo ', diffListExpo
        expoSum = sum(diffListExpo)
        print "expoSum ", expoSum

        # I'm not a huge fan of this, but it was the first thing that came to mind
        # ob1 = [a[0] for a in diffVect]
        # ob1Max = max(ob1)
        # ob2 = [a[1] for a in diffVect]
        # ob2Max = max(ob2)
        # print "i ", i, "diff vect ", diffVect
        # print "ob1 ", ob1
        # print "ob2 ", ob2
        # print "max in ob1 ", ob1Max
        # print "max in ob2 ", ob2Max
        # if len(diffVect[0]) == 3:
        #     ob3 = [a[2] for a in diffVect]
        #     ob3Max = max(ob3)
        #     print "ob3 ", ob3
        #     print "max in ob3 ", ob3Max
        print "\n"

def runDom(st, model):
    v = [part.pos for part in st.s]
    findEpsilon(model, v)
    # print 'uniq ', st.s[i].uniq, ' vel ', st.s[i].vel








