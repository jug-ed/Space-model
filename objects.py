import pymunk.pygame_util
from simulation_func import calc_moment

class Ball:
	def __init__(self, ball_mass, ball_radius, pos):
		self.mass=ball_mass
		self.radius=ball_radius
		self.body = pymunk.Body(ball_mass, calc_moment(self.mass, self.radius))
		self.body.position = pos
		self.shape = pymunk.Circle(self.body, self.radius)
		self.shape.density = 1
		self.shape.elasticity = 0.8
		self.shape.friction = 0.5

	def move(self, x, y):
		self.body.velocity = x, y
