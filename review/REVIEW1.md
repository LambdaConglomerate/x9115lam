# Review1: Week of Aug 25

## Theory

Can you define the following?

1. Evolutionary algorithms - An optimization algorithm that uses a generic population-based metaheuristic, including mutation, selection, and crossover.
   1. Genetic algorithms - A type of EA which works on flat vectors/binary strings.
   1. Genetic programming - A type of EA which works on tree structures.
1. Evolutionary programs 101
   1. Mutation - Changing one or more properties of an individual.
      1. Can you give examples of GA mutation? Of GP mutation?
            * GA mutation - change one or more values in the vector/binary string
            * GP mutation - replace a node, replace a node's information, or replace/remove a subtree
  1. Crossover - Combining attributes of different individuals.
	  1. Can you give examples of GA crossover? Of GP crossover?
	       * GA crossover - Swap values of parents past a certain point to form children.
	       * GP crossover - Swapping subtrees of the parents.
  1. Selection - Choose highly fitting individuals to survive to the next generation.
    1. Binary domination - Where an objective is never worse than any other objective and better on at least one.
    1. Pareto frontier (hint: a diagram is good here) - A set of points that all exhibit binary domination.
      1. Spread - How far apart the points on the pareto frontier are.
      1. Hypervolume - The space under the pareto frontier curve. 

____

1. Optimizing optimizers <img align=right width=400 src="http://snag.gy/Cdatd.jpg">
   (not examinable)	  
   1. Writing models: understanding and representing a domain. Very slow
   1. Enabling models: getting them running. Not fast
   1. Running them
      1. _M:_ Mutation cost: making  _M_ mutants
      2. _E_: Evaluating _M_ mutants
	     1. If any random variables in the model, then _E*20_ to _E*100*_
	  3. _S_: Selecting cost: worst case _S=M<sup>2</sup>_ comparisons
	  4. _G_: Generations: _G_ times: mutate, select, crossover, repeat
   1. Verification cost:
      1. 20 (say) repeated runs, for many models,  for many optimizers
   1. Techniques (using data mining!)
      1. _M_ cost is low. just do it,
         1. Then feed into some incremental clustering algorithm ([mini-batch k-means](http://goo.gl/V8BQs),
	        [Genic](http://papers.rgrossman.com/proc-079.pdf): [code](https://github.com/ai-se/timm/blob/ffc7071f133521014e69fc91c99aa9432510ffdb/genic.py#L5))
		 1. <img align=right src="http://snag.gy/41kWD.jpg" width=400>	Then only keep (say) a few examples per cluster, selected randomly,
		    
	   1. _E_ reductions:
	     1. In each cluster, find a handful of most different examples and just evaluate those  	 
	   1. _S_ reduction:
	     1. YOur _M_ reductions have also reduced your 	  _S=M<sup>2</sup>_ effort
	   1. _G_ remains. consider "near enough is good enough"<br clear=all>

____

1. Simulated annealing - An optimization algorithm that uses a cooling schedule to adjust how likely it is to jump around the search space.
   1. When to use SA? When you have low memory requirements.
   1. Why random jumps? We want to avoid getting stuck in local extrema.
   2. What is the cooling schedule? How the speed of cooling is adjusted over time.
      1. Why slow cooling (when you jump less and less)? As you "sober up", you jump less and less to favor local extrema. Otherwise, you would basically be doing random search.
   1. When to stop? When enough iterations have passed or you have found a solution with a sufficient energy value.
   1. Aggregation functions? A function which takes several goals and outputs a single value.
      1. Brittle aggregation functions? Aggregation functions which have equal weights for each of the goals. They can be sensitive to a particular goal which has a high variation.

## Practice

For each of the following, can you offer a 3 line code snippet to demo
the idea?

1. Classes
```python
class SA(object):
'''This class performs simulated annealling optimization'''
```
1. Functions
```python
def sum(x, y):
    return x+y
```
1. Decorators
```python
@ok
def sum_test():
    assert sum(2, 2) == 4
```
1. Static variables, functions
```
class SA(object):
    e_max = sqrt(2)
    @staticmethod
    def print_emax():
        print SA.e_max
```
1. Scope
```
foo = 5
def foobar():
    global foo
    print foo
```
  1. nested scope
```
def foo():
    foobar = "foo"
    def bar():
        foobar = "bar"
    bar()
    print foobar #"foo" is printed
```
1. functions
  1. default params
  ```python
def sum(x=2, y):
    return x+y
```
  1. variable lists args
```
def func(*args):
    sum = 0
    for arg in args:
        sum = sum + arg
    return sum
print func(1, 2, 3) #prints "6"
```
  1. variable dictionary args
```
def func2(**kwargs):
    for arg in kwargs:
        print arg, ":", kwargs[arg]
func2(foo="bar", optimizer="DE")
```
  1. lambda bodies
```
sqrt = lambda x: x**0.5
print sqrt(16) #prints "4.0"
```
1. list comprehensions
```
list = [1, 2, 3, 4, 5]
list_squared = [x**2 for x in list]
print list_squared #[1, 4, 9, 16, 25]
```
1. decorators
```
from ok import *

@ok
def foobar():
    assert 0 == 1
    
foobar() #Fails because 0 != 1
```