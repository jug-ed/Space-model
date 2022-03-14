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

#Start simulation
FPS=1
RUN=True
while RUN:
	screen.fill((0,0,0))
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()

		if i.type == pygame.MOUSEBUTTONDOWN:
			if i.button == 1:
				obj = globals()["ball%s"%str(len(objects)+1)] = Ball(1000, 60, i.pos)
				objects.append(obj)
				space.add(obj.body, obj.shape)
			if i.button == 3:
				obj = globals()["ball%s"%str(len(objects)+1)] = Ball(10, 10, i.pos)
				objects.append(obj)
				space.add(obj.body, obj.shape)

		for obj1 in objects:
			for obj2 in objects:
				if obj1 is not obj2:
					d = calc_distance(obj1, obj2)
					print(d)
					F = calc_fall_power(obj1, obj2, G, d)
					#print(F)
					#obj1.move(x, y)

		'''if i.type == pygame.KEYDOWN:
			if i.key == pygame.K_LEFT:
				shape2.move(-100, 0)
			if i.key == pygame.K_RIGHT:
				shape2.move(100, 0)
			if i.key == pygame.K_UP:
				shape2.move(0, -100)
			if i.key == pygame.K_DOWN:
				shape2.move(0, 100)'''

	space.step(1/FPS)
	space.debug_draw(draw_options)

	pygame.display.flip()
	clock.tick(FPS)