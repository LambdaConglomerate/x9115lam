from random import *
import math

class Model(object):

    def __init__(s, x):
        s.numOfVars = x
        s.constraints = []  # list of constraints
        # dict mapping decision index to constraint index in s.constraints
        s.constraintsTrack = {}
        for i in xrange(x):
            # initialising constraint tracker
            s.constraintsTrack.update({i: []})
        s.bounds = {}  # dict of bounds in the form of {index:[min, max]}
        s.objectives = []  # list of objectives
        s.name = ''

    def addName(s, name):
        s.name = name
        return s

    def addConstraint(s, indices, f):  # adds constraints
        constraintLocation = len(s.constraints)
        s.constraints.append(f)
        for i in indices:
            s.constraintsTrack[i].append(constraintLocation)
        return s

    def addBound(s, indices, min, max):  # adds bounds
        for x in indices:
            s.bounds.update({x: [min, max]})
        return s

    def addObjective(s, f):  # adds objective
        s.objectives.append(f)
        return s

    def boundy(s, index):  # generates new single random decision within bounds
        return (s.bounds[index][1] - s.bounds[index][0]) * random() + s.bounds[index][0]

    def retry(s, *args):  # generates new random vector
        vector = [s.boundy(x) for x in range(0, s.numOfVars)]
        for i in xrange(0, s.numOfVars):
            vector = s.singleRetry(vector, i)
        return vector

    # generates single random value for single index in decision within
    # contraints
    def singleRetry(s, vector, index):
        # side effect can change other indices (result of issues with Osyzka2)
        vectorConstraints = s.constraintsTrack[index]
        if(len(vectorConstraints) > 0):
            while(not reduce(lambda a, b: a & b, [s.constraints[i](vector) for i in vectorConstraints])):
                for i in xrange(0, s.numOfVars):
                    if(len([x for x in s.constraintsTrack[i] if x in vectorConstraints]) > 0):
                        vector[i] = s.boundy(i)
        else:
            vector[index] = s.boundy(index)
        return vector

    def mutate(s, vector, index):
        vector[index] = s.boundy(index)
        vector = s.singleRetry(vector, index)
        return(vector)

    def wrap(s, vector):  # wrap all values in vector
        return [(vector[i] % (s.bounds[i][1] - s.bounds[i][0])) + s.bounds[i][0] for i in range(0, len(vector))]

    def initializeObjectiveMaxMin(s, vector):
        # instantiate the max tracker for objectives
        s.objectiveMaxs = [f(vector) for f in s.objectives]
        # instantiate the min tracker for objective
        s.objectiveMins = [f(vector) for f in s.objectives]

    def updateObjectiveMaxMin(s, vector):
        values = [f(vector) for f in s.objectives]
        changed = False
        for i in range(0, len(s.objectives)):
            if(values[i] > s.objectiveMaxs[i]):
                s.objectiveMaxs[i] = values[i]
                changed = True
            if(values[i] < s.objectiveMins[i]):
                s.objectiveMins[i] = values[i]
                changed = True
        if(changed):  # if objective bounds changed
            return True  # return true so optimizer knows to update current energies
        else:
            return False

    def cal_objs(s, vect):
        return [obj(vect) for obj in s.objectives]

    def cdom(self, c1, c2, can1=None, can2=None):
        # From what I understand we could add in epsilon here
        # to determine a worthwhile difference.
        # I think we'd prob do something like this:
        # if loss(model, c1, c2) + epsilon < loss(model, c2, c1)
        # could also return something like the magnitude of the
        # difference and use that as a sort of energy value I suppose.
        a = self.loss(c1, c2)
        b = self.loss(c2, c1)
        if math.fabs(a-b) < 0.1:
            print "ZERO DIFFERENCE"
            if(can2):
                print can1
                print can2
            # else:
            #     print can1
        if(self.loss(c1, c2) < self.loss(c2, c1)):
            return True
        else:
            return False

    # Written to assume minimization
    # Menzies' code added flexibility to
    # minimize or maximize.  Figured we'd
    # just peg this for now.
    def loss(self, c1, c2):
        c1,c2 = self.cal_objs(c1), self.cal_objs(c2)
        n = min(len(c1), len(c2))
        losses = [math.exp((a - b)/n) for (a,b) in zip(c1, c2)]
        return sum(losses) / n

    def checkConstraints(s, vector):
        if(len(s.constraints) > 0):
            return reduce(lambda a, b: True & a & b, [f(vector) for f in s.constraints])
        else:
            return True

    def energy(s, v):
        d = [((f(v) - mi) / (ma - mi))**2 for f, ma,
             mi in zip(s.objectives, s.objectiveMaxs, s.objectiveMins)]
        n = reduce(lambda a, b: a + b, d)**(1 / 2.0)
        return(n / ((len(s.objectives))**(1 / 2.0)))
