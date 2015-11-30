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
    if pos in frontier:
        return
    nondom = True
    count = 0
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
        count += 1
    if nondom:
        frontier.append(pos)

def adaptiveGlobalPSO(model, retries, changes, graph=False, goal = 0.01, pat = 100, \
    era = 100, np=30, phi_1=1.5, phi_2=2.5):
    emin = 0
    phi_tot = phi_1 + phi_2
    k = (2.0/math.fabs(2.0 - (phi_tot) - math.sqrt(phi_tot**2.0 - 4.0*phi_tot)))
    s = gens(model, np)
    st = state(model.name, 'adaptiveGlobalPSO', s, 0, retries, changes, era)
    st.sb = st.s[0].pos
    bestcan = st.s[0]
    tot_deaths = 0
    while st.t:
        frontier = list()
        print "."
        st.k = changes
        while st.k:
            num_deaths = 0
            for can in st.s:
                can.vel =  [k * (vel + (phi_1 * random.uniform(0,1) * (best - pos)) + \
                 (phi_2 * random.uniform(0,1) * (gbest - pos))) \
                    for vel, pos, best, gbest in zip(can.vel, can.pos, can.pbest, st.sb)]
                can.pos = [pos + vel for pos, vel in zip(can.pos, can.vel)]
                if not model.checkBounds(can.pos) or not model.checkConstraints(can.pos):
                    can.pos = model.retry()
                    can.vel = [0.0 for x in can.pos]
                    num_deaths += 1
            tot_deaths += num_deaths
            for i in xrange(len(st.s) - 1):
                pbret = model.cdom(st.s[i].pos, st.s[i].pbest, st.s[i], st.s[i])
                if pbret == 0 or pbret == -1:
                    st.s[i].pbest = list(st.s[i].pos)
                ret_val = model.cdom(st.sb, st.s[i+1].pos, bestcan, st.s[i+1])
                if ret_val == 0:
                    st.sb = st.s[i+1].pos
                    bestcan = st.s[i+1]
                    addToFront(model,frontier,st.s[i+1].pos)
                elif ret_val == -1:
                    addToFront(model, frontier, st.s[i+1].pos)
            st.k -= 1
        for part in st.s:
            addToFront(model,frontier,part.pbest)
        f = [model.cal_objs_2(pos) for pos in frontier]
        print "f: ", f
        st.addFrontier(f)
        st.s = gens(model, np)
        st.sb = st.s[0].pbest
        bestcan = st.s[0]
        st.t -= 1
    st.termPSO()
