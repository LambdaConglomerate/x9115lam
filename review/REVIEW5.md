+ What is a Domain Specific language? Example?
    * A domain specific language is a high-level specification of knowledge that is tailored toward a particular domain. SQL is a DSL for databases.
 + What is an elbow test?
    * Whether business users understand the DSL so much that they elbow you out of the way to fix something that is wrong with it.
 + What is a context manager? Some utility code that can run before or after some other code.
   - logger - a context manager that can log the result of some code after it is executed.  
   - timer - a context manager that records the time it takes for some code to execute. [Here's](https://github.com/brouberol/contexttimer) an example of this being done.
 + Compartmental models are a visual representation of 1st order linear equation. Justify
    * Compartmental models describe the flows of stock through a system. The equation that updates a stock from its flows is something like `v.C += dt*(u.q - u.r)`, which is a first-order linear equation. There's some stuff in this [paper](http://www4.ncsu.edu/~msolufse/Compartmentmodels.pdf) that talks about this property of compartmental models.
 + What is elite sampling?
    * Picking the top X of a population.
 + Define — stocks, flows
    * Stocks: Some entity where its amount is changed over time via flows.  Have a certain value at a certain moment (ie population at a certain moment).
    * Flows: An entity that changes the amount of a stock over a period of time.  Measured per unit of time, usually some sort rate that either adds or subtrackts from stocks. (ie births per day)
 + What are auxillary variables used for?
    * They are used to handle interactions in the model that cannot be explained in terms of a stock or flow.  An example is nominal productivity below: ![](https://github.com/txt/mase/blob/master/img/brookslaw.png)
 + Name some python tools that can be used for DSLs.
    * Use [pyParsing](http://www.slideshare.net/Siddhi/creating-domain-specific-languages-in-python) (external DSL), or features of Python like decorators, context managers, and/or inheritance.
 + What is an internal DSL?
    * A DSL which uses the features of a programming language (like decorators, context managers, and inheritance for Python). The code from an internal DSL closely resembles domain syntax.  
 + Write a compartmental model for the diaper example below:
   
  ![image](https://cloud.githubusercontent.com/assets/1433964/10382520/e3319b44-6df2-11e5-994a-22702be67235.png)

```
class Diapers(Model):

  def have(i):
    return o(C = S(50), D = S(0),
             q = F(1),  r = F(5), s = F(1))

  def step(i,dt,t,u,v):
    def monday(x): return int(x) % 7 == 1
    def friday(x): return int(x) % 7 == 5
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  50  if monday(t) else 0 
    v.s  =  u.D if monday(t) else 0
    if friday(t) and t == 13: # special case (too scared to get diapers)
      v.s = 0
```

Honestly I think this code is really hard to read and understand.  Here it is with a bit more verbose variables:
```
class Diapers(Model):

  def have(i):
    return o(clean = Stock(50), dirty = Stock(0),
             inRate = Flow(1), dirtyRate = Flow(5), outRate = Flow(1))

  def step(i,timeTick,time,cur,new):
    def monday(x): return int(x) % 7 == 1
    def friday(x): return int(x) % 7 == 5
    new.clean +=  timeTick*(cur.inRate - cur.dirtyRate)
    new.dirty +=  timeTick*(cur.dirtyRate - cur.outRate)
    new.inRate  =  50  if monday(time) else 0 
    new.outRate  =  cur.dirty if monday(time) else 0
    if friday(time) and time == 13: # special case (too scared to get diapers)
      v.s = 0
```


 + Label the models below:
   
  ![cmnl](https://cloud.githubusercontent.com/assets/1433964/10382538/12b9265c-6df3-11e5-8572-7b60661e4464.jpg)

From left to right, top to bottom: "More A makes itself grow more rapidly", "More A makes B grow more rapidly", "More A, more C", "A's change consists of AF", "When A changes more, B changes more", "More AF, more C", "More C brings more change to A", "More C, more D"  

Here's the image: ![](https://github.com/txt/mase/raw/master/img/cmNl.jpg)
