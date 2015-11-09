# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
import sys

def prob(old=0.5, new=0.9, t=0, retry=0):
    if t == 0: return 0.0
    p = math.exp(((old - new) / t))
    return p

def neighbor(model, id, vector, t):
    vect = list(vector)
    bounds = model.bounds.get(id)
    decay = math.exp(-t)
    if( random() < decay):
        print 'random '
        vect = model.mutate(vect, id)
        print 's ', vector
        print 'sn ', vect
    else:
        print 'epsilon '
        mag = bounds[1] - bounds[0]
        epsilon = decay * abs(mag)
        if bool(getrandbits(1)):
            vect[id] += epsilon
        else:
            vect[id] -= epsilon
        vect = model.wrap(vect)  # wrap
    for i in range(0, len(vect)):  # check all constraints for each vector
        # will change value if constraints aren't met
        vect = model.singleRetry(vect, i)
        # could implement this differently
    return(vect)


def cdom(model, c1, c2):
    # From what I understand we could add in epsilon here
    # to determine a worthwhile difference.
    # I think we'd prob do something like this:
    # if loss(model, c1, c2) + epsilon < loss(model, c2, c1)
    # could also return something like the magnitude of the
    # difference and use that as a sort of energy value I suppose.
    if loss(model, c1, c2) < loss(model, c2, c1):
        return True
    else:
        return False

# Written to assume minimization
# Menzies' code added flexibility to
# minimize or maximize.  Figured we'd
# just peg this for now.
def loss(model, c1, c2):
    c1,c2 = model.cal_objs(c1), model.cal_objs(c2)
    n = min(len(c1), len(c2))
    losses = [math.exp((a - b)/n) for (a,b) in zip(c1, c2)]
    return sum(losses) / n

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
def sac(model, retries, changes, goal = 0.01, pat = 100, era = 100):
    emin = 0
    s = model.retry()
    model.initializeObjectiveMaxMin(s)
    for i in xrange(1000):
        # prime the maxs and mins with second values, avoids divide by 0
        model.updateObjectiveMaxMin(model.retry())
    st = state(model.name, 'SAC', s, model.energy(s), retries, changes, era)
    print 'model name ', model.name
    #changes is some static value passed by the caller
    #st changes is actually a counter
    while st.t:
        st.k = changes
        patience = pat
        while st.k:
            # An Energy based stopping condition
            # doesn't make sense here.
            # 1st possible stopping condition
            # close to the minimum
            # if st.eb - emin <= goal:
            #     st.sbo = st.sb
            #     st.eb = model.energy(st.sb)
            #     st.ebo = model.energy(st.sbo)
            #     st.term()
            #     return
            # 2nd stopping condition
            # We've had the same best for
            # a long while.
            # This still makes sense since we can just
            # check if the vector is the same, if it is
            # it hasn't been dominated in quite awhile.
            if st.sb == st.sblast:
                if patience == 0:
                    st.bored()
                    st.k = 0
                    break
                else:
                    patience -= 1
            else:
                patience = pat
                st.sblast = list(st.sb)
            c = randint(0, model.numOfVars - 1)
            st.sn = neighbor(model, c, st.s, st.k / changes)
            if(model.updateObjectiveMaxMin(st.sn)):  # check if new objective bounds
                st.e = model.energy(st.s)  # adjust accordingly
                st.eb = model.energy(st.sb)
                st.ebo = model.energy(st.sbo)
            best = cdom(model, st.sn, st.sb)
            better = cdom(model, st.sn, st.s)
            st.en = model.energy(st.sn)
            if(best):
                st.app_out('!')
                st.sb = list(st.sn)
                st.eb = st.en
            if(better):
                st.app_out('+')
                st.s = list(st.sn)
                st.e = st.en
            # This is just pegged so that the old is better than the new
            # I'm using pretty small values here.  The actual aggregated values
            # are much larger, so obviously this isn't going to work exactly right
            # the whole point though is just to test out cdom.
            elif(prob(st.e, st.en,((changes - st.k)/changes), st.t) < random()):
                st.app_out('?')
                st.s = st.sn
                st.e = st.en
            else:
                st.app_out('.')
            st.k -= 1
        # First check if the sb for that set of changes was better
        # Than any of our other retries
        ultimate = cdom(model, st.sb, st.sbo)
        if(ultimate):
            st.app_out(' ^')
            st.sbo = list(st.sb)
            st.ebo = st.eb
        # Then retry with a brand new set of values
        st.s = model.retry()
        st.sn = list(st.s)
        st.sb = list(st.sn)
        st.e = model.energy(st.s)
        st.en = st.e
        st.eb = st.en
        st.t -= 1
    st.term()
