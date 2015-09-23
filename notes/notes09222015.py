# Re pushes back
# Prior to Toronto group (Myopolis et al) requirements weren't considered in SE, people like Djikstra said requirements weren't part of SE
# Local search: surf the turf (moto of maxwalksat -> sample the search space around the current solutions because water runs down hill)
# maxwalksat does two things either sample around current space or jump to new space
# maxwalksat is an example of local search
# SA can mutate any number of decisions while maxwalksat only mutates one

# Schaffer min(f1 + f2) at x = 1
# Fun with Fonseca


# gadgetgetsok.txt -> coded SA by Menzies (line 248)
# contextmanager called Study -> prints time, prints all the magic constants, epsilon 
# tiles -> prints quantile distribution
# prints f1 scores -> after SA values have gone down
# prints f2 scores -> medians ahve gone down after SA
# Fonsica has problem -> issue with the model, it's basically flat: talke to user, can also use elite sampling where the values can influence your next choice (a king of heuristic search)
# ZDT1 -> SA is kicking butt and taking names
# you have to reflect as much on the models as the optimizers

# fromHell-> hell: 1,1 heaven: 0,0 : we can express as distance from heaven or distance from hell
# normalize with sqrt(2) 
# from heaven is a smaller space(exploring smaller space)
# from hell is larger (exploring a larger space), preferrable because we are about options, we want to present users with range of options, possibly solutions they never thought of

# Model project -> how to build a model
# business user who is knowlegable and wants to build a model

# Doman-Specific Languages 101: https://github.com/txt/mase/blob/master/src/dsl101.md
# Compartmental modeling: stocks and flows, tubes carry stuff to tubs
# linked book has compartmental model ("Software Process Dynamics" - Raymond J.Madachy)
# Does you language pass the elbow test -> do business users elbow you out of the way to change something wrong on the screen
# can you abstract the business knowledge, allow busines users do the coding, if business users cannot elbow you out the way you've lost something
# All the little languages 
# Read Godel, Esher, Bach
# From 1967 -> needed programming languages that are as natural as possible
# DSL is a high level language that user can learn in less than a day
# Ideoms: Methods imposed by programmers to handle common forms
# External DSLs are hard (compilers) string is manipulated and evaluated
# Internal DSLs are easier
# Python decorators: @ok
# Decorators run from top to bottom
# Logger and timer are tiny examples of an idiom, wrapping up common processes\
# Watch implementing domain specific languages in python

# Have to understand semantics of the thing you are modeling 
# Stock is something that is/are, a quantity that exists at a certain time
# Flow is something that changes, measured at a per interval of time (rates)
# Sometimes after stocks and flows we need auxillaries, for example (adding new people to a SW project slows the rate)
# Diapers is a subclass of model
# have is an initialization of the model and returns constraints
# u is the last time tick, payload at time t
# v is the next time tick, payload at time t+1
# this model fills in v from u
# the the step method dt is the time tick, don't model continuous time we model little steps in time
# t is the current time
# add to u the time tick time * (inflow - outflow)
# Exam question: given a compartmental model write downt he python with the v and u
# o is the payload (2 stocks, 3 flows)
# restrain clips the highs
# wrap a bunch of stuff around step to handle timing, going to negative, etc..

# state and keys:
# state is knowledge about constraints
# keys sorts state 

# Even though domain specific languages is general models, it's an exmaple of making python business user readable



#python below here about 
#context managers have yields in the middle
from contextlibe import contextmanager
import time
@contextmanager
def timeit():
	start = time.time()
	try:
		yield
	finally:
		print("It took", time.time() - start, "seconds")

#this might take a few seconds
with timeit():
	list(range(10000000))

#with runs up to yield in timeit then executes list and print finally pritn
#variables set before the yield are available after its
#yield returns control
#python context manager is way to handle the code before and code after

