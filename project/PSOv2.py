from Models import *
from random import *
from state import *
from grapher import *
import sys, random, math, copy, operator

class can(can):

    def __init__(self, *args, **kwargs):
        super(can, self).__init__(*args, **kwargs)
        self._radius = 1.0 #this is a multiplier

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

def gens(model, np, personalListSize):
    init_pos = [model.retry() for x in xrange(np)]
    init_vel = [[0.0 for _ in xrange(len(init_pos[i]))] for i, val in enumerate(init_pos)]
    init_bpos = [[model.retry() for x in xrange(personalListSize)] for i in xrange(np)]
    init_ids = [i for i in xrange(np)]
    cans =list()
    for i in xrange(np):
        cans.append(can(init_pos[i], init_vel[i], init_bpos[i], init_ids[i]))
        # cans = [can(pos, vel, pbest, uniq) for pos, vel, pbest, uniq in zip(init_pos, init_vel, init_bpos, init_ids)]
    return cans

#euclidean distance
def distance(v1, v2):
    return sum([(a + b)**2.0 for a, b in zip(v1, v2)])**(1/2.0)

#calculate repulsion
def repulsion(c1, c2, radius):
    #coulomb's law, tinker with constant
    constant = 2.0
    force = constant * c1.radius * c2.radius / (radius**2.0)
    return force

def PSOv2(model, retries, changes, graph=False, goal = 0.01, pat = 100, \
era = 100, np=30, phi_1=3.8, phi_2=2.2, personalListSize=5):
    g = grapher(model, int(retries), 1, changes)
    emin = 0
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs((2.0 - phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    #k = 0.25
    print k
    vmax = max([(x[1] - x[0]) for x in [model.getBounds(i) for i in range(model.numOfDecisions())]])
    baseRadius = vmax/float(model.numOfDecisions())

    s = gens(model, np, personalListSize)
    st = state(model.name, 'adaptiveGlobalPSO', s, 0, retries, changes, era)
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
        # model.initializeObjectiveMaxMin(st.sb)
        # for c in st.s:
        #     model.updateObjectiveMaxMin(c.pos)
        st.k = changes
        #iterative loop
        while st.k:
            if st.k % 100 == 0:
                print "="*29
                print "k ", st.k
                print "tot_deaths ", tot_deaths
            num_deaths = 0
            uniqTracker = list()
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + \
                 (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest[0], frontier[0])]
                # print 'can.vel ', can.vel
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                #V2 logic here
                #tracks to make sure we are not doubling up
                uniqTracker.append(can.uniq)
                for c in st.s:
                    if c.uniq in uniqTracker: 
                        continue
                    else:
                        radius = distance(c.pos, can.pos)
                        #stop crowding my space 
                        if(radius < baseRadius):
                            newRadius = (c.radius + can.radius)**(0.5)
                            #print(newRadius)
                            c.radius = newRadius
                            can.radius = newRadius
                                
                        #always repulse for a little jitter
                        repulsedVelocity = repulsion(c, can, radius)
                        #print("repulsed force=" + str(repulsedVelocity))
                        can.vel = [repulsedVelocity * vmax + vel for vel in can.vel]
                        can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                        #instead of resetting wiggle 
                        #each index until bounds and constraints
                        #are met
                        for i in xrange(len(can.pos)):
                            can.pos = model.singleRetry(can.pos, i)

                        #other particle will repulse the opposite direction    
                        c.vel = [-repulsedVelocity * vmax + vel for vel in c.vel]
                        c.pos = [pos + vel for pos, vel in zip(c.pos, c.vel)]
                        for i in xrange(len(c.pos)):
                            c.pos = model.singleRetry(can.pos, i)

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

        for can in st.s:
            print(str(can.uniq)+ " radius = " + str(can.radius) + " energy = " + str(model.energy(can.pbest[0])))
        st.s = gens(model, np, personalListSize)
        st.sb = st.s[0].pbest
        bestcan = st.s[0]
        st.t -= 1
        # print 'final front ', [model.cal_objs_2(f) for f in frontier]
        for f in frontier:
            global_frontier.append(f)
            g.addVector(f, int(st.t))
        frontier = runDom(st,model,list())
        # for v in st.s:
        #     g.addVector(v.pbest[0], v.uniq)
    for f in global_frontier:
        st.reg_front.append(model.cal_objs_2(f))
        st.norm_front.append(model.cal_objs(f))
    g.graph()
    g.graphEnergy()
    g.graphTrackedParticle()
    st.termPSO()


def dominate(model, setOfPos, pruning=10):
    max_index = 0
    # objs = list()
    while len(setOfPos) > pruning:
        objs = [model.cal_objs(pos) for pos in setOfPos]
        expoSumList = list()
        for i in xrange(len(objs)):
            # print i
            diffVect = [[objs[j][k] - objs[i][k] for k in xrange(len(objs[i]))] for j in xrange(len(objs)) if j != i]
            # print 'diffVect ', diffVect
            # listOfTruth = [[(objs[i][k] - diffVect[i][k] <= objs[j][k]) for k in xrange(len(objs[i]))] for j in xrange(len(objs)) if j != i]
            # print 'any list ', any(listOfTruth)
            diffList = [max(v) for v in diffVect]
            # print 'diffList ', diffList
            # print "len ", len(diffList)
            diffListExpo = [-math.exp(-val/k) for val in diffList]
            # print 'diffListExpo ', diffListExpo
            expoSum = sum(diffListExpo)
            expoSumList.append(expoSum)
            # print "expoSum ", expoSum
            # print "\n"
        # print '\n'
        # print 'expoSumList ', expoSumList
        # print '\n'
        # purloined from here: http://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
        min_index, min_value = min(enumerate(expoSumList), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(expoSumList), key=operator.itemgetter(1))
        # print 'min score ', min_value, 'min objective vals ', objs[min_index]
        # print 'max score ', max_value, 'max objective vals ', objs[max_index]
        setOfPos.pop(min_index)
        # print '\n'
        # print 'max idx ', max_index
        # print '\n'
        # print 'setOfPos after pop ', setOfPos, 'Set of pos length after pop ', len(setOfPos)
    # print 'objs ', objs
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
    # print '\n'
    # print 'finalSet ', setOfPos
    return setOfPos

def runDom(st, model, frontier, globalListSize=10, personalListSize=5):
    #for pbests
    # print 'st.s ', st.s
    for part in st.s:
        # print '\n'
        part.pbest.append(part.pos)
        part.pbest = dominate(model, part.pbest, personalListSize)
    # first add the current positions of all
    # particles to their pbestlist
    # then run the list for each of them through
    # the domination proceedure
    for part in st.s:
        frontier.append(part.pbest[0])
    # print 'frontier before ', frontier
    frontier = dominate(model, frontier, globalListSize)
    # print 'frontier after ', frontier
    # vel = [x.vel for x in st.s]
    # print 'velocities ', vel
    return frontier








