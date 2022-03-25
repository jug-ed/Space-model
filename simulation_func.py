import pymunk.pygame_util, math
from math import sqrt

def calc_moment(mass, radius):
	return pymunk.moment_for_circle(mass, 0, radius)

def calc_distance(obj1, obj2):
	return sqrt((obj1[0] - obj2[0])**2 + (obj1[1] - obj2[1])**2)

def calc_fall_power(obj1, obj2, G, d):
	try:
		return G*((obj1.mass/obj2.mass)/(d**2))
	except ZeroDivisionError:
		return 0
