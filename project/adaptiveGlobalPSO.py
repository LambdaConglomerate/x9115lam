from Models import *
from random import *
from state import *
from grapher import *
import sys, random, math, copy, operator

def gens(model, np, personalListSize):
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.0 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = [[model.retry() for x in xrange(personalListSize)] for i in xrange(np)]
    init_ids = [i for i in xrange(np)]
    cans =list()
    for i in xrange(np):
        cans.append(can(init_pos[i], init_vel[i], init_bpos[i], init_ids[i]))
    return cans

def adaptiveGlobalPSO(model, retries, changes, graph=False, goal = 0.01, pat = 100, \
era = 100, np=30, phi_1=2.8, phi_2=1.2, personalListSize=5, out = 'out.txt'):
    g = grapher(model, int(retries), 1, changes)
    emin = 0
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    s = gens(model, np, personalListSize)
    st = state(model.name, 'adaptiveGlobalPSO', s, 0, retries, changes, era, out=out)
    st.sb = st.s[0].pos
    bestcan = st.s[0]
    tot_deaths = 0
    model.initializeObjectiveMaxMin(st.sb)
    for c in st.s:
        model.updateObjectiveMaxMin(c.pos)
    frontier = runDom(st, model, list())
    # basic idea is this is a list of positions that
    # persist between retries.
    global_frontier = list()
    #retry loop
    while st.t:
        print "."
        st.k = changes
        #iterative loop
        while st.k:
            if st.k % 100 == 0:
                print "="*29
                print "k ", st.k
                print "tot_deaths ", tot_deaths
            num_deaths = 0
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + \
                 (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest[0], frontier[0])]
                # print 'can.vel ', can.vel
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                if not model.checkBounds(can.pos) or not model.checkConstraints(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.1 for x in can.pos]
                    num_deaths += 1
                model.updateObjectiveMaxMin(can.pos)
            tot_deaths += num_deaths
            g.trackParticle(st.s[0].pos, 0, st.k)
            # for v in st.s:
            #     g.addVector(v.pos, v.uniq)
            runDom(st, model, frontier)
            st.k -= 1
        st.s = gens(model, np, personalListSize)
        st.sb = st.s[0].pbest
        bestcan = st.s[0]
        for f in frontier:
            st.app_out(str(model.cal_objs_2(f)) + '\n')
            global_frontier.append(f)
            g.addVector(f, int(st.t))
        frontier = runDom(st,model,list())
        st.t -= 1
        # for v in st.s:
        #     g.addVector(v.pbest[0], v.uniq)
    for f in global_frontier:
        st.reg_front.append(model.cal_objs_2(f))
        st.norm_front.append(model.cal_objs(f))
    # g.graph()
    # g.graphEnergy()
    # g.graphTrackedParticle()
    st.termPSO()

def dominate(model, setOfPos, pruning=10):
    max_index = 0
    while len(setOfPos) > pruning:
        objs = [model.cal_objs(pos) for pos in setOfPos]
        expoSumList = list()
        for i in xrange(len(objs)):
            diffVect = [[objs[j][k] - objs[i][k] for k in xrange(len(objs[i]))] for j in xrange(len(objs)) if j != i]
            diffList = [max(v) for v in diffVect]
            diffListExpo = [-math.exp(-val/k) for val in diffList]
            expoSum = sum(diffListExpo)
            expoSumList.append(expoSum)
        # purloined from here: http://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
        min_index, min_value = min(enumerate(expoSumList), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(expoSumList), key=operator.itemgetter(1))
        setOfPos.pop(min_index)
    # Weird phenonmena: the max gets shoved either to the end or beginning
    # of the list fairly frequently and if we pop it off then the idx is wrong
    if max_index == len(setOfPos):
        max_index -= 1
    # swap the best position to the top of the list
    # don't really need it to be sorted, just need the
    # best
    tmp = setOfPos[0]
    setOfPos[0] = setOfPos[max_index]
    setOfPos[max_index] = tmp
    return setOfPos

def runDom(st, model, frontier, globalListSize=10, personalListSize=5):
    for part in st.s:
        part.pbest.append(part.pos)
        part.pbest = dominate(model, part.pbest, personalListSize)
    for part in st.s:
        frontier.append(part.pbest[0])
    frontier = dominate(model, frontier, globalListSize)
    # vel = [x.vel for x in st.s]
    # print 'velocities ', vel
    return frontier








