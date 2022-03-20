import pygame, pymunk.pygame_util, math
from math import sqrt
from objects import Ball
from simulation_func import calc_distance, calc_fall_power

#Settings window
pygame.init()
size = (800,800)
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
clock = pygame.time.Clock()

#Settings space
pymunk.pygame_util.positive_y_is_up = False
draw_options = pymunk.pygame_util.DrawOptions(screen)
space = pymunk.Space()
space.gravity = 0, 0
G = 6.67
x, y = 0, 0

#Objects
objects = []
dedicated_object = None

#Start simulation
FPS=60
RUN=True
while RUN:
	try:
		screen.fill((0,0,0))

		for obj1 in objects:
			if dedicated_object != obj1 and obj1.radius >= calc_distance(obj1.body.position, pygame.mouse.get_pos()): dedicated_object = obj1
			for obj2 in objects:
				if obj2 is not obj1:
					d = calc_distance(obj1.body.position, obj2.body.position)
					#print(d)
					F = calc_fall_power(obj1, obj2, G, d)
					#print(F)
					pygame.draw.line(screen, (255,255,255), obj1.body.position, obj2.body.position, 1)

		for i in pygame.event.get():
			if i.type == pygame.QUIT:
				exit()

			if i.type == pygame.MOUSEBUTTONDOWN:
				if i.button == 1:
					dedicated_object.info()
				if i.button == 3:
					dedicated_object.body.apply_impulse_at_world_point([0,1000], [0,0])
				if i.button == 6:
					obj = globals()["ball%s"%str(len(objects)+1)] = Ball(1000, 60, i.pos)
					objects.append(obj)
					space.add(obj.body, obj.shape)
				if i.button == 7:
					obj = globals()["ball%s"%str(len(objects)+1)] = Ball(10, 10, i.pos)
					objects.append(obj)
					space.add(obj.body, obj.shape)
				if i.button == 4:
					print("Up")
				if i.button == 5:
					print("Down")

			if i.type == pygame.KEYDOWN:
				if i.key == pygame.K_LEFT:
					dedicated_object.move(-100, 0)
				if i.key == pygame.K_RIGHT:
					dedicated_object.move(100, 0)
				if i.key == pygame.K_UP:
					dedicated_object.move(0, -100)
				if i.key == pygame.K_DOWN:
					dedicated_object.move(0, 100)

		space.step(1/FPS)
		space.debug_draw(draw_options)

		pygame.display.flip()
		clock.tick(FPS)
	except AttributeError:
		pass