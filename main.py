import  pygame, math
from math import sqrt
from tkinter import *
from tkinter import messagebox

#colors
RED = (122,0,0)
GREEN = (28, 94, 28)
BLUE = (6,18,148)
PURPLE = (84, 37, 120)
ORANGE = (184, 70, 0)
CORAL = (173, 102, 57)
GRAY = (75,76,84)
YELLOW = (255,216,107)
BLACK = (0,0,0)

#settings
info_visible = False
PLAY=PAUSE = True
i=j=bn = 0

#simulator settings
size = (0,0)
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
cntr_x = int(size[0]/2)
cntr_y = int(size[1]/2)

def createPlanet():
    try:
        clr = (int(color_entry.get().split(',')[0]),int(color_entry.get().split(',')[1]),int(color_entry.get().split(',')[2]))
        globals()["%s"%name_entry.get()] = Planet(
            name_entry.get(),
            float(size_entry.get()),
            clr,
            float(orbit_entry.get()),
            objects[objPiv_list.curselection()[0]]
            )
        objects.append(globals()["%s"%name_entry.get()])
        objPiv_list.insert(len(objects)+1, name_entry.get())
    except:
        pass

#menu settings
menu = Tk()
menu.geometry('350x550')
menu.title('Menu')
label = Label(menu, text='Create planet', font=('',36))
name_label = Label(menu, text='Name', font=('',16))
name_entry = Entry(menu, font=('',14))
size_label = Label(menu, text='Size', font=('',16))
size_entry = Entry(menu, font=('',14))
color_label = Label(menu, text='Color (x,x,x)', font=('',16))
color_entry = Entry(menu, font=('',14))
objPiv_label = Label(menu, text='Object pivot', font=('',16))
objPiv_list = Listbox(menu)
orbit_label = Label(menu, text='Orbit', font=('',16))
orbit_entry = Entry(menu, font=('',14))
create = Button(menu, text='Create', font=('', 16), command=createPlanet)
label.pack()
name_label.pack()
name_entry.pack()
size_label.pack()
size_entry.pack()
color_label.pack()
color_entry.pack()
objPiv_label.pack()
objPiv_list.pack()
orbit_label.pack()
orbit_entry.pack()
create.pack()


class Star:
    def __init__(self, name, size, bias_x, bias_y, color):
        self.name = name
        self.size = size
        self.bias_x = bias_x
        self.bias_y = bias_y
        self.color = color
        self.x = 0
        self.y = 0
        self.info_size = size

    def info(self):
        messagebox.showinfo(f'Star {self.name}', f'Size: {self.info_size}\nColor: {self.color}\nPosition: ({self.x}, {self.y})')

    def draw(self):
        self.x = cntr_x + self.bias_x
        self.y = cntr_y + self.bias_y
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


class Planet:
    def __init__(self, name, size, color, orbit, obj_pivot):
        self.name = name
        self.size = size
        self.color = color
        self.orbit = orbit + size + obj_pivot.size
        self.r = 0
        self.x = 0
        self.y = 0
        self.obj_pivot = obj_pivot
        self.speed = 31 / (orbit * (2 * 3.14))
        self.info_size = size
        self.info_orbit = orbit

    def info(self):
        messagebox.showinfo(f'Planet {self.name}', f'Size: {self.info_size}\nColor: {self.color}\nOrbit: {self.info_orbit}\nPosition: ({self.x}, {self.y})')

    def move(self):
        if PLAY:
            if self.r <= 360:
                angle = self.r * (3.14/180)
                self.x = (self.orbit + self.obj_pivot.size) * math.cos(angle) + self.obj_pivot.x
                self.y = (self.orbit + self.obj_pivot.size) * math.sin(angle) + self.obj_pivot.y
                self.r += self.speed
            else:
                self.r = 0
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


#objects
Solar = Star('Solar', 130, 0, 0, YELLOW)
Mercury = Planet('Mercury', 4, GRAY, 57, Solar)
Venus = Planet('Venus', 12, CORAL, 100, Solar)
Earth = Planet('Earth', 12, GREEN, 149, Solar)
Moon = Planet('Moon', 3, GRAY, 30, Earth)
Mars = Planet('Mars', 6, RED, 227, Solar)
Jupiter = Planet('Jupiter', 139, ORANGE, 778, Solar)
Saturn = Planet('Saturn', 116, PURPLE, 1400, Solar)
Uranus = Planet('Uranus', 50, BLUE, 2800, Solar)
Neptune = Planet('Neptune', 49, BLUE, 4400, Solar)

objects = [Solar, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune]

for obj in objects:
    objPiv_list.insert(len(objects)+1, obj.name)


clock = pygame.time.Clock()
FPS  = 300
FULLSCREEN = False
RUN = True
while RUN:
    #frame rate per second
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    #control
    keys = pygame.key.get_pressed()
    #pause
    if keys[pygame.K_SPACE] and PAUSE:
        if PLAY == False:
            PLAY = True
        else:
            PLAY = False
        PAUSE = False
    elif keys[pygame.K_SPACE] != True:
        PAUSE = True
    #moving
    if keys[pygame.K_LEFT]:
        cntr_x += 1
    elif keys[pygame.K_RIGHT]:
        cntr_x -= 1
    if keys[pygame.K_UP]:
        cntr_y += 1
    elif keys[pygame.K_DOWN]:
        cntr_y -= 1
    #zoom
    if keys[pygame.K_LSHIFT]:
        for obj in objects:
            obj.size += (obj.size/100)
            if obj.__class__ == Planet:
                obj.orbit += (obj.orbit/100)
    elif keys[pygame.K_LCTRL]:
        for obj in objects:
            obj.size -= (obj.size/100)
            if obj.__class__ == Planet:
                obj.orbit -= (obj.orbit/100)
    #full/window screen
    if keys[pygame.K_F12]:
        if FULLSCREEN == False:
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            FULLSCREEN = True
        else:
            screen = pygame.display.set_mode(size,pygame.RESIZABLE)
            FULLSCREEN = False

    #info about objects
    for obj in objects:
        mouse_position = pygame.mouse.get_pos()
        distance = sqrt((mouse_position[0] - obj.x)**2 + (mouse_position[1] - obj.y)**2)
        if distance <= obj.size:
            if pygame.mouse.get_pressed()[0] and info_visible != True:
                info_visible = True
                obj.info()
            if pygame.mouse.get_pressed()[0] != True:
                info_visible = False

    #collision of objects
    for obj1 in objects:
        for obj2 in objects:
            distance = sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
            if distance <= obj1.size + obj2.size:
                if obj1.name != obj2.name:
                    if bn > 250:
                        objects.remove(obj1)
                        objects.remove(obj2)
                    bn+=1

    #rendering all objects
    screen.fill(BLACK)
    try:
        Solar.draw()
        for obj in objects:
            if obj.__class__ == Planet:
                obj.move()
            else:
                obj.draw()
    #if object size too big
    except OverflowError:
        for obj in objects:
            obj.size -= (obj.size/100)*10
            if obj.__class__ == Planet:
                obj.orbit -= (obj.orbit/100)*10

    pygame.display.update()
    try:
        menu.update()
    except TclError:
        menu.mainloop()
menu.mainloop()