# Notes for var names:
# f = some anonymous function
# x = some value
# i = some index
from Models import *
from random import *
from state import *
import sys

def prob(old, new, t):
    p = math.exp(((old - new) / t))
    print 'p: ', p
    return p

def neighbor(model, id, vector, t):
    vect = list(vector)
    bounds = model.bounds.get(id)
    decay = math.exp(-t)
    if( random() < decay):
        vect = model.singleRetry(vect, id)
    else:
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
def sa(model, retries, changes, goal = 0.01, pat = 100, era = 100):
    emin = 0
    s = model.retry()
    model.initializeObjectiveMaxMin(s)
    for i in xrange(1000):
        # prime the maxs and mins with second values, avoids divide by 0
        model.updateObjectiveMaxMin(model.retry())
    st = state(model.name, 'SA', s, model.energy(s), retries, changes, era)
    #changes is some static value passed by the caller
    #st changes is actually a counter
    while st.t:
        st.k = changes
        patience = pat
        while st.k:
            # 1st possible stopping condition
            # close to the minimum
            if st.eb - emin <= goal:
                st.sbo = st.sb
                st.eb = model.energy(st.sb)
                st.ebo = model.energy(st.sbo)
                st.term()
                return
            # 2nd stopping condition
            # We've had the same best for
            # a long while.
            if st.eb == st.eblast:
                if patience == 0:
                    st.bored()
                    st.k = 0
                    break
                else:
                    patience -= 1
            else:
                patience = pat
                st.eblast = st.eb
            c = randint(0, model.numOfVars - 1)
            st.sn = neighbor(model, c, st.s, st.k / changes)
            if(model.updateObjectiveMaxMin(st.sn)):  # check if new objective bounds
                st.e = model.energy(st.s)  # adjust accordingly
                st.eb = model.energy(st.sb)
                st.ebo = model.energy(st.sbo)
            st.en = model.energy(st.sn)
            if(st.en < st.eb):
                st.app_out('!')
                st.sb = st.sn
                st.eb = st.en
            if((st.en < st.e)):
                st.app_out('+')
                st.s = st.sn
                st.e = st.en
            elif(prob(st.e, st.en, st.k / changes) > random()):
                st.app_out('?')
                print 'took route'
                st.s = st.sn
                st.e = st.en
            else:
                st.app_out('.')
            st.k -= 1
        # First check if the sb for that set of changes was better
        # Than any of our other retries
        if(st.eb < st.ebo):
            st.app_out(' ^')
            st.sbo = list(st.sb)
            st.ebo = st.eb
        # Then retry with a brand new set of values
        st.s = model.retry()
        st.e = model.energy(st.s)
        st.sn = list(st.s)
        st.en = st.e
        st.sb = list(st.sn)
        st.eb = st.en
        st.t -= 1
    st.term()
