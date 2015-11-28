# Introduction #
Particle swarm optimization (PSO) is an optimization technique inspired by the "murmurations" of swarms of birds. Each candidate in a PSO swarm relies on its own knowledge of the domain space as well as the collective knowledge of the swarm. The simple baseline implementation of PSO provided by the authors [1] to first coin the technique leaves plenty of opportunities for the addition of heuristics, which may improve the performance of PSO. We experimented with a few tweaks and heuristics to see if they give better results than the classical version by Kennedy and Eberhart.

# Related Work #
## The Classical Model ##
The origins of PSO and its "classical" implementation are provided by Kennedy and Eberhart [1]. Each candidate is at a random position in decision space, and moves via a change in position due to its velocity, which can change every timestep. The velocity is determined by a few factors. The first is the best position that each candidate has visited, stored in `pbest`. The second is the best position that has ever been visited by any candidate, stored in `gbest`. Third is the candidate's current position `presentx`. Fourth is a stochastic measure which the authors coin as "craziness". Last is the candidate's current velocity `vx`, which helps preserve the candidate's momentum. 

The local and global best each have the same weight so they affect the new velocity the same. The authors opened this area up for future researchers to find optimal weights. The "craziness" factor is multiplied by two so candidates will overshoot the goal about half the time.

# References
[1] http://www.cs.tufts.edu/comp/150GA/homeworks/hw3/_reading6%201995%20particle%20swarming.pdf