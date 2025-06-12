class Camera:
    def __init__(self, scale=1.0, offset_x=0, offset_y=0):
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y

    def world_to_screen(self, pos):
        return int((pos[0] + self.offset_x) * self.scale), int((pos[1] + self.offset_y) * self.scale)

    def zoom_in(self, step, min_scale=0.1):
        self.scale += step

    def zoom_out(self, step, min_scale=0.1):
        self.scale = max(min_scale, self.scale - step)

    def move_left(self, step):
        self.offset_x += step / self.scale

    def move_right(self, step):
        self.offset_x -= step / self.scale

    def move_up(self, step):
        self.offset_y += step / self.scale

    def move_down(self, step):
        self.offset_y -= step / self.scale
