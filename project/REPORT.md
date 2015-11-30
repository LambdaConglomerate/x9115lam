# Introduction #
Particle swarm optimization (PSO) is an optimization technique inspired by the "murmurations" of swarms of birds. Each candidate in a PSO swarm relies on its own knowledge of the domain space as well as the collective knowledge of the swarm. The simple baseline implementation of PSO provided by the authors [1] to first coin the technique leaves plenty of opportunities for the addition of heuristics, which may improve the performance of PSO. We experimented with a few tweaks and heuristics to see if they give better results than the classical version by Kennedy and Eberhart.

# Related Work #
## The Classical Model ##
The origins of PSO and its "classical" implementation are provided by Kennedy and Eberhart [1]. Each candidate is at a random position in decision space, and moves via a change in position due to its velocity, which can change every timestep. The velocity is determined by a few factors. The first is the best position that each candidate has visited, stored in `pbest`. The second is the best position that has ever been visited by any candidate, stored in `gbest`. Third is the candidate's current position `presentx`. Fourth is a stochastic measure which the authors coin as "craziness". Last is the candidate's current velocity `vx`, which helps preserve the candidate's momentum.

The local and global best each have the same weight so they affect the new velocity the same. The authors opened this area up for future researchers to find optimal weights. The "craziness" factor is multiplied by two so candidates will overshoot the goal about half the time.

## The Adaptive Model ##
In the classical model, there is equal weight given to the local best (aka the cognitive learning rate) and the global best (aka the social learning rate). Yuhui Shi and Russell Eberhart [2] developed an inertia weight 'w' factor to balance the local and global search to obtain better performance.

In 2002, Maurice Clerc and James Kennedy [3] explored PSO from the particle's perspective and gained some unique insights, one of which was the introduction of constriction coefficients to keep the particles together. They experimented with constriction on a few benchmark functions and were able to find minima on some very complex functions, on up to thirty dimensions.

## Parameter Tuning ##
Due to the many parameters of classical PSO, tuning these parameters is a must to get good results. A well-known paper by Anthony Carlisle and Gerry Dozier [4] does just that. Their goal was to give recommendations for the parameters that future researchers could use as a good baseline to get up and running. They found that a good population size was 30, a global neighborhood was better than a local neighborhood, asynchronous updates were less costly than synchronous updates,

# References
[1] http://www.cs.tufts.edu/comp/150GA/homeworks/hw3/_reading6%201995%20particle%20swarming.pdf

[2] http://dsp.szu.edu.cn/pso/ispo/download/a%20modified%20pso.pdf

[3] http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=985692&url=http%3A%2F%2Fieeexplore.ieee.org%2Fiel5%2F4235%2F21241%2F00985692

[4] https://github.com/timm/sbse14/wiki/etc/pdf/Off-The-Shelf_PSO.pdf
