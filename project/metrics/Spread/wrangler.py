path = "./True_PF/ZDT"

for i in xrange(1,6):
  if i == 5:
    continue
  print i
  fn = path + str(i) +".txt"
  f = open(fn, "r")
  ln = f.readline()
  fin = ''
  while ln:
    print ln
    ln = ln.strip()
    arr = ln.split()
    ln = " ".join(arr)
    fin += ln + '\n'
    ln = f.readline()
  f.close()

  f = open(fn, "w")
  f.write(fin)
