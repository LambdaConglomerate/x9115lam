from swampy.TurtleWorld import *
import math

# Setting stop=0 makes stop an optional argument
# with default value 0
def polygon(t, length, num_sides, stop=0):
  angle = 360.0 / num_sides
  if stop:
    num_sides = stop
  for i in range(num_sides):
    fd(t, length)
    lt(t, angle)

def arc(t, radius, theta):
  circumference = 2 * math.pi * radius
  arc_length = (theta / 360.0) * circumference
  # Could refactor per the book to define based
  # on circumference, but not running slow enough
  # to bother
  num_sides = 100
  seg_length = circumference / num_sides
  # Calculates the number of sides to draw
  # to reach the correct arc_length
  stop = arc_length / seg_length
  polygon(t, seg_length, num_sides, int(stop))

def circle(t, radius):
  arc(t, radius, 360)
  # circumference = 2 * math.pi * radius
  # num_sides = 100
  # length = circumference / num_sides
  # polygon(t, length, num_sides)

def flower():
  num_petals = 20.0
  angle_increment = 360.0 / num_petals
  for i in range (42):
    # arc(bob, 10, 15)
    # lt(bob, 90)
    arc(bob, 150, 30)
    lt(bob, 135)
    if(i % 2 == 0):
       lt(bob, 15)

  wait_for_user()

def flower1():
  for i in range (8):
    arc(bob, 50, 90)
    lt(bob, 135)

def flower2():
  for i in range (20):
    arc(bob, 50, 90)
    lt(bob, 90)
    if(i % 2 == 0):
      lt(bob, 36)

world = TurtleWorld()
bob = Turtle()

# Make bob fast
bob.delay = 0.01




flower()
# arc(bob, 50, 180)
# circle(bob, 20)
# polygon(bob, 100, 6)
