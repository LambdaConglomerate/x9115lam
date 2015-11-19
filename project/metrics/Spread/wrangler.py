fn = "./True_PF/Tanaka.txt"
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
