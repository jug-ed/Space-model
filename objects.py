import pymunk

class SpaceBody:
    def __init__(self, space, x, y, mass=100, radius=15):
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass=mass, moment=moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        space.add(self.body, self.shape)

    @property
    def position(self):
        return self.body.position

    @property
    def velocity(self):
        return self.body.velocity

    @property
    def radius(self):
        return self.shape.radius

    @property
    def mass(self):
        return self.body.mass
    