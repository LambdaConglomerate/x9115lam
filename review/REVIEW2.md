# Review2: Week of Sept 5

##  Practice

### 1. Iterators

1a. The following code has a bug. The countdown stops at 10 (no 9,8,7...). Why?

```python
def countdown(n):
   while n >= 0:
     return  n
     n -= 1

print("We are go for launch")
for x in countdown(10):
   print(x)
print("lift off!")
```

The countdown stops at 10 because of the return statement. For this function to work properly, `return` should be replaced with `yield`.

1b. Modify the following code such that the final `out` list
only contains numbers over 20

```python
def items(x, depth=-1):
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y, depth+1):
        yield z
  else:
  yield _,x

out = []
for _,x in items(  [10,[ 20,30],
                        40,
                        [   (  50,60,70),
                            [  80,90,100],110]]):
   out += [x]
return out
``` 
Before `out += [x]`, add `"if [x]" > 20`.

1c. Repeat the above, this time using _list comprehensions_.
Before `return out`, add `out = [x for x in out if x > 20]`

1d. Using list comprehensions, write a function that returns only non-whitespace
in a string. Hint:

```python
import string
string.whitespace # <== contains all whitespace chars
```
```
def string_no_whitespace(str):
    return [s for s in str if s not in string.whitespace]
```

```

```
1e. Using list comprehensions and the following code,
return all lines in a multi-line
strings that  are (a) non-blanks and (b) longer than 20
lines. Hints: `not str` returns `True` for non empty strings.

```python
def lines(string):
  tmp=''
  for ch in string: 
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch 
  if tmp:
  yield tmp
```
```
str = [x for x in lines("abcdksjfa;lksadjfadsf;\ndef\n\nghi") if x and len(x) > 20]
      
for s in str:
    print s
```
The blocks above doesn't work actually.  It only takes the length of the currently passed back string from the lines function.  The following function works:

```
def mul_line(str):
  ret = [s for s in lines(str) if s]
  if(len(ret) > 20):
    print ret
```

There's a file in the same directory as this .md file (lines.py) that shows how the other one doesn't work.  There isn't a way that I can think of to do this only with list comprehensions.

### 2. Dunders


2a. What are the dunders in the following code? For each one,
use them in a code snippet.

```
class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
```

The dunders are `__init__`, `_setitem__`, `__getitem__`, and `__repr__`. 

```
obj = o(foo="bar")
obj["foo"] = "foobar"
print obj["foo"]
print obj
```

2b. In the above, what is the magic __dict__ variable?

A mapping of instance variables to their values.

2c. What would happen if the _last line_ in the following `__iadd__` method
was deleted?

```python
r = random.random
rseed = random.seed

class Some:
  def __init__(i, max=8): 
    i.n, i.any, i.max = 0,[],max
  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:    
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x 
    return i
```	
`None` would be returned.

2d. In English, explain what the above `Some` class  does. Use it in a loop
to keep `Some` numbers in the series 0,1,2,...999.

The `Some` class keeps a certain number of items in a list. After the list has been filled to capacity, adding a new item will replace a random item in the list.