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
    spaces_to_insert = 70 - len(s)
    for i in range(0, spaces_to_insert):
        print " ",
        
    print(s)

right_justify('allen')