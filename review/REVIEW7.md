# Review 7: Differential Evolution

- Explain: DE's build new examples by extrapolating between known ones.
	* The idea is that we start off with a pool of randomly generated candidates and then actually extrapolate based on that field of candidates.  Each new candidate is extrapolated from the following function new = x + f(y-z). So we are using some preexisting x and then extrapolating that x based on two other candidates in the field.  If new is better than the old x then we replace it, otherwise we keep the old x, and iterate through the entire field of candidates doing the same thing.  So we start with a field and then just extrapolate based on that original field until we stop.
- Explain the following DE constants:
- What is np and how is it used?
	* NP is the number of candidates.  This value doesn't change throughout running DE.  There is always a limited population of some preset value.  Generally NP = 10 * num_decisions.
- What is cf and how is it used?
	* cf is the probability with which cross-over will occur.  When we go into the extrapolate function we check to see if a random value is less than the probability of cross-over, if true we cross-over according to the function new = x + f * (y-z).  Suggestion is to start at cf = 0.3, and then switch to cf [0.8, 1] if nothing happens.
- What is f and how is it used?  F is a preset constant for how much to actually extrapolate.  Looking at the equation above it is really a weight on how much to add to the value of candidate x, based on the value of candidate y minus candidate z.  In the paper [here](http://download.springer.com.prox.lib.ncsu.edu/static/pdf/382/art%253A10.1023%252FA%253A1008202821328.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.1023%2FA%3A1008202821328&token2=exp=1444659682~acl=%2Fstatic%2Fpdf%2F382%2Fart%25253A10.1023%25252FA%25253A1008202821328.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.1023%252FA%253A1008202821328*~hmac=87ff9ff368fea8d67ef1ebda1175738f7ead5af15ab8f9088dfe7d998ffdceed) Storn defines it as a real constant factor in the range [0,2].  But per menzies the value is actually chosen in a range [0.5, 1] and a higher NP should denote a lower F.
- Write down, in 10 lines or less, pseudo-code for DE.
```
def candidate():
  something = [lo(d) + n(hi(d) - lo(d)) 
               for d in decisions()])
  new = Thing()
  new.have  = something
  new.score = score(new)
  return new

def n(max):
  return int(random.uniform(0,max))

class Thing():
  id = 0
  def __init__(self, **entries): 
   self.id = Thing.id = Thing.id + 1
   self.__dict__.update(entries)

def de(max     = 100,  # number of repeats 
       np      = 100,  # number of candidates
       f       = 0.75, # extrapolate amount
       cf      = 0.3,  # prob of cross-over 
       epsilon = 0.01
       ):
  frontier = [candidate() for _ in range(np)] 
  for k in range(max):
    total,n = update(f,cf,frontier)
    if total/n > (1 - epsilon): 
      break
  return frontier

 def update(f,cf,frontier, total=0.0, n=0):
  for x in frontier:
    s   = x.score
    new = extrapolate(frontier,x,f,cf)
    if new.score > s:
      x.score = new.score
      x.have  = new.have
    total += x.score
    n     += 1
  return total,n

def extrapolate(frontier,one,f,cf):
  out = Thing(id   = one.id, 
              have = copy(one.have))
  two,three,four = threeOthers(frontier,one)
  changed = False  
  for d in decisions():
    x,y,z = two.have[d], three.have[d], four.have[d]
    if rand() < cr:
      changed = True
      new     = x + f*(y - z)
      out.have[d]  = trim(new,d) # keep in range
  if not changed:
    d      = a(decisions())
    out.have[d] = two[d]
  out.score = score(out) # remember to score it
  return out 

#Returns three different things that are not 'avoid'.
def threeOthers(lst, avoid):
  def oneOther():
    x = avoid
    while x.id in seen: 
      x = a(lst)
    seen.append( x.id )
    return x
  # -----------------------
  seen = [ avoid.id ]
  this = oneOther()
  that = oneOther()
  theOtherThing = oneOther()
  return this, that, theOtherThing


def a(lst) :
  return lst[n(len(lst))]

 ```

- Distinguish between the following two kinds of DE algorithms:
    + DE/rand/1
    	* The function is new = x + f * (y-z).  
    + DE/best/2
    	* The function is new = Xbest + F * (A + B - Y - Z), such that A,B,Y,Z are candidtates selected at random. 
    + The main difference here is that instead of using a ranomly selected x and then extrapolating based on that x we are actually choosing the best candidate overall and then extrapolating based on it.  Also we are using more candidates for the extrapolation than before.  There are four candidates used for the extrapolation funciton where in rand/1 we only use two.







