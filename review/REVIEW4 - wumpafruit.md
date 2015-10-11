What is the problem with local maxima?

1. In the following diagram, each square has the same x,y,z axis. What might the names of those x,y,z values?
![](https://github.com/timm/sbse14/wiki/etc/img/landscape/WrightFitness.jpg)

    * x: length of hair
    * y: body weight
    * z: probability of winning a fight

2. Explain the following, using the above diagram:

 * Holes - areas with low fitness
 * Poles - areas with high fitness
 * Saddles - the flat space between a hole and a pole
 * Local minima - an area that seems optimal but really isn't
 * Flat - a landscape that has roughly the same terrain. You will spend a lot of time traversing it before you find something interesting.
 * Brittle - a landscape that has many poles. In order to achieve better goals you might have to give up on your current solution.

3. Explain the following term and describe how it handles the problem of flat: Retries
    * Retries allow the search an opportunity to start over and forget what it has already done. In a flat landscape, good solutions are hard to come by. So if you are spending a lot of time searching but not finding any good results, retrying is a method to essentially start over and hope that the next time you find a good solution.

4. How do the following techniques avoid the problems of local maxima?
    - **Simulated annealing:** Early on in the search, SA is very likely to wander around the search space. If SA is on a local maxima, it is likely to jump somewhere else even though this point may be the best it has encountered so far.
    - **Retries:** Retries don't directly avoid the problems of local maxima. If a local maxima isn't "good enough", it will simply start the search over, hoping to find a better solution. Basically, if you encounter a maxima that isn't "good enough", try again until you do.
    - **Momentum** (make sure you explain momentum): Momentum allows a search to continue past a point where it would normally stop to see if there are any better solutions there. Momentum might carry a local search past a local maxima to an even better solution. 
5. Local search can be characterized as follows

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

```
c = random part of solution 
IF    p < random()
THEN  change a random setting in c
ELSE  change setting in c that maximizes score(solution) 
```