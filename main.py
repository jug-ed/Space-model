import pygame, pymunk.pygame_util, math, threading
from math import sqrt
from tkinter import *
from tkinter import messagebox
from objects import Ball, Menu
from simulation_func import calc_distance, calc_fall_power

#Start simulation
def start_simulation(scr_width, scr_height):
	#Settings window
	pygame.init()
	size = (scr_width,scr_height)
	screen = pygame.display.set_mode(size,pygame.RESIZABLE)
	clock = pygame.time.Clock()

	#Settings space
	pymunk.pygame_util.positive_y_is_up = False
	draw_options = pymunk.pygame_util.DrawOptions(screen)
	space = pymunk.Space()
	space.gravity = 0, 0
	G = 6.67

	#Settings menu
	window = Tk()
	window.withdraw()

	#Objects
	objects = []
	dedicated_object = None
	selected_object = None
	def create_obj(mass, radius, pos):
		obj = globals()["ball%s"%str(len(objects)+1)] = Ball(mass, radius, pos)
		objects.append(obj)
		space.add(obj.body, obj.shape)

	FPS=60
	PLAY=False
	RUN=True
	while RUN:
		try:
			screen.fill((0,0,0))

			for obj1 in objects:
				if dedicated_object != obj1 and obj1.radius >= calc_distance(obj1.body.position, pygame.mouse.get_pos()): dedicated_object = obj1
				if obj1 != selected_object:
					obj1.shape.color = (255,255,255,0)
				x = y = 0
				for obj2 in objects:
					if obj2 is not obj1:
						d = calc_distance(obj1.body.position, obj2.body.position)
						#print(d)
						F = calc_fall_power(obj1, obj2, G, d)
						#print(F)
						pygame.draw.line(screen, (255,255,255), obj1.body.position, obj2.body.position, 1)
						x = (obj1.body.position[0] - obj2.body.position[0]) * F
						y = (obj1.body.position[1] - obj2.body.position[1]) * F
						if PLAY:
							obj2.move(x/100, y/100)
						else:
							obj2.stop()

			for i in pygame.event.get():
				if i.type == pygame.QUIT:
					exit()

				if i.type == pygame.MOUSEBUTTONDOWN:
					if i.button == 1:
						dedicated_object.info()
					if i.button == 3:
						if selected_object != None and selected_object == dedicated_object:
							objects.remove(selected_object)
							space.remove(selected_object.body, selected_object.shape)
							selected_object = dedicated_object = None
						selected_object = dedicated_object
						selected_object.shape.color = (100,100,100,0)
					if i.button == 6:
						create_obj(10000, 60, i.pos)
					if i.button == 7:
						create_obj(10, 10, i.pos)
					if i.button == 4:
						print("Up")
					if i.button == 5:
						print("Down")

				if i.type == pygame.KEYDOWN:
					if i.key == pygame.K_TAB:
						pass
					if i.key == pygame.K_LEFT:
						selected_object.move(-1000,0)
					if i.key == pygame.K_RIGHT:
						selected_object.move(1000,0)
					if i.key == pygame.K_UP:
						selected_object.move(0,-1000)
					if i.key == pygame.K_DOWN:
						selected_object.move(0, 1000)
					if i.key == pygame.K_SPACE:
						if PLAY == True: PLAY = False
						else: PLAY = True

			space.step(1/FPS)
			space.debug_draw(draw_options)

			pygame.display.flip()
			clock.tick(FPS)
		except AttributeError:
			pass


if __name__ == "__main__":
	simulation1 = threading.Thread(
				target=start_simulation,
				args=(800,800)
				)
	simulation1.start()