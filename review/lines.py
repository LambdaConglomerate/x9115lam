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

def mul_line(str):
  ret = [s for s in lines(str) if s]
  if(len(ret) > 20):
    print ret

def mul_line_fail(str):
  ret = [s for s in lines(str) if s and len(s) > 20]
  print ret


str1 = "Lorem ipsum dolor sit amet,\n consectetur adipiscing elit.\n Fusce tempus magna sit amet\n libero hendrerit\nornare. Suspendisse\n in tempus\nec\
 risus, eu \nlobortis urna. Etiam mollis vehicula velit vitae rutrum.\n Duis et tellus enim. Vestibulum in laor\neet diam. Ut mollis m\naximus quam.\
  Aliquam era\nt volutpat. Aliqua\nm sit amet erat rhoncu\ns, tempus mauris ut, \ninterdum sem. Ut\n rhoncus ut lacus at\n eleifend. Viv\namus at\
   condimen\ntum\n est.\n Nulla\n nec lac\ninia odio."
str2 = 'al;dskfjaskl;dfjkl;asdjfkl;asjdfkl;jasdfkl;jsdfl;jsdfl;kjsdfl;kjasdfl;kjasdfl;kjsdfl;'

print 'success'
mul_line(str1)
mul_line(str2)

print 'failure'
mul_line_fail(str1)
mul_line_fail(str2)
