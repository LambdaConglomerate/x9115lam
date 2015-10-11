
What is the problem with local maxima?

Many search spaces are not convex and have many local maxima. In optimization problems, search algorithms may not find the global maximum if they have poor initialization conditions and converge to a local maximum and not the most optimal solution. This leads to a solution being over-adapted/over-specialized to a local maxima. 

1. In the following diagram, each square has the same x,y,z axis. What might the names of those x,y,z values?
![](https://github.com/timm/sbse14/wiki/etc/img/landscape/WrightFitness.jpg)

x = length of hair
y = body weight
z = probability of winning fight

2. Explain the following, using the above diagram:

 * Holes
A dip in the search space 
 * Poles
 Mountains in the search space
 * Saddles
Flat space between a pole(mountain) and a holeW hen all eigenvalues are real and at least one of them is positive and at least one is negative. Saddles are always unstable.
 * Local minima 
A point in the sample space whose all adjacent spaces are higher.
 * Flat
A section of the sample space with no changes. Cannot bing anything better of worse.
 * Brittle
 A solution that works well for a very exact environment but becomes significantly worse if there are slight pertubations to the environment.

3. Explain the following term and describe how it handles the problem of flat: Retries.
Searching locally in a flat solution space does not lead to good progress. Good solutions may be seperated by large distances. Retries leap large distances to a new space and start over overcoming the issues with flat spaces. 

4. How does the following techniques avoid the problems of local maxima?

  Simulated annealing
    - Retries
Retries jump to 
    - Momentum (make sure you explain momentum)
  
5. Local search can be charac terized as follows

   + Jump all around the hills
   + Sometimes, sitting still while rolling marbles left and right
   + Then taking one step along the direction where the marbles roll the furthest.
   + Go to 1.

In the following code snippet, explain where you'd find 5.
```
FOR i = 1 to max-tries DO
  solution = random assignment
  FOR j =1 to max-changes DO
    IF  score(solution) > threshold
        THEN  RETURN solution
    FI
    c = random part of solution 
    IF    p < random()
    THEN  change a random setting in c
    ELSE  change setting in c that maximizes score(solution) 
    FI
RETURN failure, best solution found
```


