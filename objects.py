import pymunk.pygame_util
from tkinter import *
from tkinter import messagebox
from simulation_func import calc_moment
from pymunk.vec2d import Vec2d

class Menu(Tk):
	def __init__(self):
		pass


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
		self.body.apply_impulse_at_world_point([x,y], [0,0])

	def info(self):
		messagebox.showinfo("Info", f"Mass: {self.mass}\nRadius: {self.radius}\nPosition: {self.body.position}")
		#print(f"Mass: {self.mass}")
		#print(f"Radius: {self.radius}")
		#print(f"Position  x:{self.body.position[0]}  y:{self.body.position[1]}\n")