
### Simulated Annealing

  1. In a few lines, define ordered and unordered search. In what way are they different?
  * Ordered search is where the solution spreads out in a wave over some solution space.
  * Unordered search is where a partial solution is quickly generated then fiddled with.
  * Ordered search is designed for a solution that has a particular ordering, where current decisions affect future ones. Unordered search is useful where ordering does not matter.
  2. In a few lines, compare and contrast: (1) Greedy search; (2) Local Search; and (3) Stochastic search. What, if any, are the trade-offs in using a Stochastic search?
        * Greedy search will choose the locally best option, local search changes a part of the current solution which increases the score the most, and stochastic search changes part of the current solution at random. Stochastic search by itself cannot guarantee an optimal solution because all it makes are random changes. However, there is a greatly higher chance or exploring the search space with stochastic search than with greedy search.
  3. In about 10 lines, write down the pseudo-code for SA. Number each line.
  ```
  1 def SA(s_0):
  2     s = s_0, e = energy(s), sb = s, eb = e, k = 0
  3     while k < kmax and e > emax:
  4         sn = neighbor(s); en = energy(sn)
  5         if en > eb:
  6             eb = en; sb = sn
  7         elif en < e or P(e, en, k/kmax) > rand():
  8             s = sn; e = en
  9         k = k+1
  10    return sb
  ```
  4. In the pseudo-code for SA, you used a neighbourhood function `Neighbour()`. Write down an expression for this.
  `return [s[0]+-e, s[1]+-e,...]`
  5. 4. In the pseudo-code for SA, you used a probability function `P(e_new, e_old, t)`. What would be a valid mathematical expression for this?
  ```
  e^((e_old-e_new)/t)
  ```
  6. With respect to function `P(e_new, e_old, t)`, justify the following statements:
      * Initially, SA is like a drunk, then it sobers up.
        * Initially, `t` is very low, so the expression above evaluates to a high number. On line 7 in #3, this means that we are more likely to consider solutions that are worse than the current solution. We are staggering around ("like a drunk"). Over time, `t` approaches 1, which makes the probability function lower. This means that we will not consider worse solutions as much ("it sobers up").
      * SA consumes lower memory.
        * The probability function itself is very simple and easy to understand. It does not use any memory of itself. It is simply working with the parameters that are passed in. It also means that we do not keep track of every solution that is generated. We only know the best solution, the current solution, and the neighboring solution.
  7. How would you terminate a stochastic algorithms such as SA sooner? (*HINT: Look at variances of epochs*)
        * We could either make e_max higher (lower the energy requirement) or decrease k_max (lower the maximum number of steps).
  8. When finding a solution, you can either mutate towards ''Heaven'' (A better spot) or you can choose to mutate away from "Hell" (A worse spot). Why would you choose one over the other? (*HINT: One of them has a better diversity of search.*)
        * Distance from hell has better diversity of search than distance from heaven. Distance from hell is preferred because of this, since you can not only give a point with a certain distance, but you can give a greater variance of other points with that same distance than you could by using distance from heaven.