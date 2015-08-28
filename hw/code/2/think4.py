from swampy.TurtleWorld import *
import math

# Stop is just the number of sides to draw
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
  # Could base on circumference, but not bothering
  num_sides = 100
  seg_length = circumference / num_sides
  stop = arc_length / seg_length
  polygon(t, seg_length, num_sides, stop=int(stop))

def circle(t, radius):
  arc(t, radius, 360)

def petal(t, radius, angle):
  for i in range (2):
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
  diagonal_angle = diag_angle(num_sides, length)
  diag = diag_length(num_sides, length, diagonal_angle)
  triangle_peak = 180 - (diagonal_angle + 90)
  lt(t, diagonal_angle)
  fd(t, diag)
  if(num_sides % 2 != 0):
    for i in range (num_sides - 1):
      lt(t, triangle_peak)
      fd(t, diag)
      lt(t, 180)
      fd(t, diag)
  else:
    for i in range (num_sides - 1):
      lt(t, diagonal_angle * 2)
      fd(t, diag)
      lt(t, 180)
      fd(t, diag)

def clear_bob(delay):
  world = TurtleWorld()
  bob = Turtle()
  bob.delay = delay
  return bob

def draw_flowers():
  # Flower1
  flower(clear_bob(0.01), 7, 40.0, 100.0)
  # Flower2
  flower(clear_bob(0.01), 10, 90.0, 100.0)
  # Flower3
  flower(clear_bob(0.01), 20, 18, 250.0)

def draw_pies():
  for i in range (3):
    pie(clear_bob(0.1), 50, (i + 5))
  wait_for_user()

def main():
  bob = Turtle()
  draw_flowers()
  draw_pies()

main()


# arc(bob, 50, 180)
# circle(bob, 20)
# polygon(bob, 100, 6)
