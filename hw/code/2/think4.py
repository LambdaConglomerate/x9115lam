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

def petal(t, radius, angle):
  arc(t, radius, angle)
  lt(t, 180 - angle)
  arc(t, radius, angle)
  lt(t, 180 - angle)

def flower(t, num_petals, petal_angle, radius):
  angle_increment = 360.0 / num_petals
  for i in range (int(num_petals) ):
    petal(t, radius, petal_angle)
    lt(t, angle_increment)

def diag_length(num_sides, length, diagonal_angle):
  diagonal_angle = math.radians(diagonal_angle)
  diagonal = (length / 2) / math.cos(diagonal_angle)
  return diagonal

def diag_angle(num_sides, length):
  sum_int_angles = 180 * (num_sides - 2)
  int_angle = sum_int_angles / num_sides
  diagonal_angle = int_angle / 2
  return diagonal_angle

def pie(t, length, num_sides):
  polygon(t, length, num_sides)

  # diag = (.5 * length)/.59
  diagonal_angle = diag_angle(num_sides, length)
  diag = diag_length(num_sides, length, diagonal_angle)
  triangle_peak = 180 - (diagonal_angle + 90)
  lt(t, diagonal_angle)
  fd(t, diag)
  for i in range (num_sides - 1):
    lt(t, triangle_peak)
    fd(t, diag)
    lt(t, 180)
    fd(t, diag)

  wait_for_user()

# def flower1():
#   for i in range (8):
#     arc(bob, 50, 90)
#     lt(bob, 135)

# def flower2():
#   for i in range (20):
#     arc(bob, 50, 90)
#     lt(bob, 90)
#     if(i % 2 == 0):
#       lt(bob, 36)

world = TurtleWorld()
bob = Turtle()
bob.delay = 0.1
pie(bob, 50, 9)




def draw_flowers():
  # Flower1
  world.clear()
  bob = Turtle()
  bob.delay = 0.01
  flower(bob, 7, 40.0, 100.0)

  # Flower2
  world.clear()
  bob = Turtle()
  bob.delay = 0.01
  flower(bob, 10, 90.0, 100.0)

  # Flower3
  world.clear()
  bob = Turtle()
  bob.delay = 0.01
  flower(bob, 20, 18, 250.0)


# arc(bob, 50, 180)
# circle(bob, 20)
# polygon(bob, 100, 6)
