from Models import *
from random import *
from state import *
import sys


def say(x):
    sys.stdout.write(str(x))
    sys.stdout.flush()

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
def mws(model, retries, changes, goal = 0.01, pat = 100, era = 100):
    emin = 0
    s = model.retry()
    model.initializeObjectiveMaxMin(s)
    # prime the maxs and mins with values, avoids divide by 0
    for i in xrange(1000):
        model.updateObjectiveMaxMin(model.retry())
    st = state(model.name, 'MWS', s, model.energy(s), retries, changes, era)
    while st.t:
        st.k = changes
        patience = pat
        while st.k:
            # 1st possible stopping condition
            # close to the minimum
            if st.eb - emin <= goal:
                st.sbo = st.sb
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
            if(random() >= 0.5):
                st.sn = model.mutate(st.s, c)
                if(model.updateObjectiveMaxMin(st.sn)):
                    st.e = model.energy(st.s)  # update all energies if new normal
                    st.eb = model.energy(st.sb)
                    st.ebo = model.energy(st.sbo)
            else:
                tempS = list(st.sn)
                tempE = model.energy(st.sn)
                for index in range(1, 10):
                    tempS[c] = (model.bounds[c][1] -
                                model.bounds[c][0]) * (index / 10.0)
                    if(model.checkConstraints(tempS)):
                        if(model.updateObjectiveMaxMin(tempS)):
                            # update all energies if new normal
                            st.e = model.energy(st.s)
                            st.eb = model.energy(st.sb)
                            st.ebo = model.energy(st.sbo)
                            st.en = model.energy(st.sn)
                            tempE = model.energy(tempS)
                        if(model.energy(tempS) < tempE):
                            st.sn = list(tempS)
                            tempE = model.energy(tempS)
            st.en = model.energy(st.sn)
            if st.en < st.eb:
                st.sb = list(st.sn)
                st.eb = st.en
                st.app_out('!')
            if st.en < st.e:
                st.app_out('+')
            else:
                st.app_out('.')
            # Always promote the last solution
            st.s = list(st.sn)
            st.e = st.en
            st.k -= 1
        # First check if the sb for that set of changes was better
        # Than any of our other retries
        if(st.eb < st.ebo):
            st.sbo = list(st.sb)
            st.ebo = st.eb
            st.app_out('^')
            # Then retry with a brand new set of values
        st.s = model.retry()
        st.e = model.energy(st.s)
        st.sn = list(st.s)
        st.en = st.e
        st.sb = list(st.sn)
        st.eb = st.en
        st.t -= 1
    st.term()
