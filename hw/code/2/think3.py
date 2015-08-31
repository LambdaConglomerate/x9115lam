# 3.1
# repeat_lyrics()
# def print_lyrics():
#     print "I'm a lumberjack, and I'm okay."
#     print "I sleep all night and I work all day."

# def repeat_lyrics():
#     print_lyrics()
#     print_lyrics()

# 3.2
def repeat_lyrics():
    print_lyrics()
    print_lyrics()

def print_lyrics():
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."

repeat_lyrics()

# 3.3
def right_justify(s):
    # For some reason the solution here before printed
    # tabs instead of simple spaces printing to out.txt
    # gives the last character of allen in the 70th column
    print ' '*(70 - len(s)) + s
    # for i in range(0, spaces_to_insert):
    #     print " "
    # print(s)

right_justify('allen')

#3.4
def do_twice(f, val):
    f(val)
    f(val)

def print_spam():
    print 'spam'

def print_twice(s):
    print s
    print s

def do_four(f, val):
    do_twice(f, val)
    do_twice(f, val)

do_four(print_twice, 'spam')

#3.5
def print_2x2_grid():
    print "+ - - - - + - - - - +"
    do_twice(print_twice, "|         |         |")
    print "+ - - - - + - - - - +"
    do_twice(print_twice, "|         |         |")
    print "+ - - - - + - - - - +"

def print_4x4_grid():
    print "+ - - - - + - - - - + - - - - + - - - - +"
    do_twice(print_twice, "|         |         |         |         |")
    print "+ - - - - + - - - - + - - - - + - - - - +"
    do_twice(print_twice, "|         |         |         |         |")
    print "+ - - - - + - - - - + - - - - + - - - - +"
    do_twice(print_twice, "|         |         |         |         |")
    print "+ - - - - + - - - - + - - - - + - - - - +"
    do_twice(print_twice, "|         |         |         |         |")
    print "+ - - - - + - - - - + - - - - + - - - - +"

print
print_2x2_grid()

print
print_4x4_grid()
