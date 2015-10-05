Our output for this program is in out.txt.  And a screenshot of the output is shown below:

![output](./img/MaxWalkOut.png)

For reading the output T is the retry number that we are on in the iterations.  Each retry lasts for 1000 changes, then we take the best solution out of that retry and add it as our best if it is the best overall.  SB is the best solution for that run, EB is the energy of that best solution when calculating energy 'From Hell' so a max energy value is square root of 2.

Finally SBO at the end of the run is the best solution overall and EBO is the best energy overall.