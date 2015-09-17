#not sure if this compiles it's from the chalkboard
#fib closures
def memo(f):		
	cache = {}
	def wrappedfunction(*args, **d):	#list of args, list of keyword arguments, generic call for any python function 
		if n in cache:
			return cache[n]
		else:
			tmp = f(*args, **d)
			cache[n] = tmp
			return tmp
	return wrappedfunction

@memo
def fib(n):
	if n < 2:
		return 1
	else:
		return f(n-2) + f(n-1)


#first class object functions
@memo
def lt(x,y):
	return x < y

def gt(x,y):
	return x > y

def check(x, y, better=lt):
	return 	better(x, y)

# SA
# candidate solutions: 1. decisions 2. objectives 3. aggregates(optional)
# candidate = decisions + objectives + aggregates(optional)
# Schaffer has 1 decision = x, 2 objectives = f1, f2, aggregate = from_hell_measure
# Quantile chart from notes:
# 	each line is an era
# 	each line is a summary of the f1 scores from each line above

# Relax video
# Multi-objective overtime planning paper
# 	vector with work packages, n tasks with each task having a certain amount overtime
# 	each candidate is a set of decisions with a certain amount of overtime
# 	took NSGAII and made simple change
# 	2 point crossover apply max and min
# 	changes to a model are big changes, putting domain knowledge into models is very powerful


# Goals
# 	Goal-based modeling summary 
# 	Traceability: map to summary(requirements document), does the code satisfy the requirements, 10^7 LOC train!, smart!
# 	Runtime Verification:	10^6 LOC, train!!, smart!!
# 	Model Checking: return crash or no, if I can find a pathway to an error 10^4 LOC, train!!!, smart!!!
# 	Theorem Proving: will crash if it runs our of memory 10^3, train!!!!, smart!!!!

# Requirements engineering people
# 	user requirements are comical 
# 	Myopoulous, Fickas, Lamsweerde are researches who analyse human wims
# 	We can explore conflicting human ideals

# MaxWalkSat
# 	small change to SE
# 	by code 6 we should be able to pass any model into our optimizers, don't be clever for code 4 or code 5
# 	Sampling the landscape of the local region, peaks at the curve
# 	Jumps anywhere at random half the time
# 	The shape of the data is more important than the algorithm, some shapes of data can defeat any algorithm
# 	We live in an n-dimensional space, 50 year old men know where the closest bathroom is
# 	We are in a space of dimensions proportional the amount decisions we can make
# 	Rabbits, shapes determine what we can optimize, not the optimization algorithm
# 	We are worried about spaces where a small changes can have dramatic consequences
# 	I can't prove things by looking at the source code of optimizer I have to look at the shape of the data
# 	MaxWalkSat -> sometimes focus of just one dimension
# 	Latin demo -> like sodoku but with color, random solves problem while deterministic gets stuck
# 	MaxWalkSat changed the face of AI, let us solve problems orders of magnitude bigger than before
# 	It finds a landscape
# 	If you have a vector of decisions than random jumps to one of the values (will be on exam)



